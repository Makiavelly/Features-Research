"""Independent H&M flat-table experiment with same data/pools and explicit base controls."""
import ast
import hashlib
import json
from pathlib import Path
import textwrap

HERE=Path(__file__).resolve().parent
D=HERE/'flat_variant'
base=json.loads((HERE/'llmfe_llama31_hm_kaggle_t4.ipynb').read_text(encoding='utf-8'))
original=(HERE/'worker.py').read_text(encoding='utf-8')
def node_source(source,node):return ''.join(source.splitlines(keepends=True)[node.lineno-1:node.end_lineno])+'\n'
data_class=next(n for n in ast.parse(original).body if isinstance(n,ast.ClassDef) and n.name=='Data')
history_data='import json\nfrom pathlib import Path\nimport pandas as pd\nimport numpy as np\n'+node_source(original,data_class)
guard_source=(HERE/'balance_diagnostic/worker.py').read_text(encoding='utf-8')
guard='import ast\nimport re\n'
for n in ast.parse(guard_source).body:
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FORBIDDEN' for t in n.targets) or isinstance(n,ast.FunctionDef) and n.name=='extract':
        guard+=node_source(guard_source,n)
worker=original
for n in reversed(ast.parse(worker).body):
    if getattr(n,'name',None) in {'Data','matrix','check_program','compile_program'}:
        lines=worker.splitlines(keepends=True);del lines[n.lineno-1:n.end_lineno];worker=''.join(lines)
worker=worker.replace("RAW = '''def modify_features(X, history):\n    return pd.DataFrame(index=X.index)\n'''",
    'from flat_features import RAW, SEED, RAW_ONLY, Data, matrix, compile_program, check_program')
worker=worker.replace('len(names)==len(data.raw_u+data.raw_i)',"not getattr(func,'_feature_changed',False)")
checked_lines=[]
for line in worker.splitlines(keepends=True):
    if line.strip()=='_,names=matrix(data,sample,func,expected=names)':
        prefix=line[:len(line)-len(line.lstrip())]
        checked_lines.extend(prefix+s+'\n' for s in [
            'values,names=matrix(data,sample,func,expected=names)',
            'middle=len(sample)//2',
            'halves=np.concatenate([matrix(data,sample.iloc[:middle],func,expected=names)[0],matrix(data,sample.iloc[middle:],func,expected=names)[0]])',
            "if not np.array_equal(values,halves,equal_nan=True):raise ValueError('Features depend on batch size or other rows; use rowwise transformations only')"])
    else:checked_lines.append(line)
worker=''.join(checked_lines)
worker=worker.replace("['train','search'", "['train','search'")
runtime=(HERE/'runtime.py').read_text(encoding='utf-8')
runtime=runtime.replace('from worker import RAW, check_program, Data, map_at_12',
    'from worker import RAW, check_program, Data, map_at_12\nfrom flat_features import SEED, RAW_ONLY, normalize')
ps=(D/'prompts.py').read_text(encoding='utf-8');definitions=ast.parse(ps).body
for n in reversed(ast.parse(runtime).body):
    new=next((d for d in definitions if isinstance(d,ast.FunctionDef) and d.name==getattr(n,'name',None)),None)
    if new:
        lines=runtime.splitlines(keepends=True);lines[n.lineno-1:n.end_lineno]=node_source(ps,new).splitlines(keepends=True);runtime=''.join(lines)
runtime=runtime.replace('memories=[[raw.copy()] for _ in range(3)]','''seed_dir=out/'seed_control';seed_dir.mkdir(exist_ok=True)
    (seed_dir/'program.py').write_text(SEED)
    seed_score=evaluate(data,seed_dir,'search',config)
    seed={'directory':str(seed_dir),'score':seed_score['map']}
    raw15_dir=out/'raw15_control';raw15_dir.mkdir(exist_ok=True)
    (raw15_dir/'program.py').write_text(RAW_ONLY)
    raw15_score=evaluate(data,raw15_dir,'search',config)
    raw15={'directory':str(raw15_dir),'score':raw15_score['map']}
    memories=[[raw.copy(),seed.copy()] for _ in range(3)]''')
runtime=runtime.replace('prompt(data,[raw],42+proposal)','prompt(data,[seed],42+proposal)')
runtime=runtime.replace('if key in seen:', 'if key in seen or key in {source_key(RAW),source_key(SEED),source_key(RAW_ONLY)}:')
runtime=runtime.replace('options=[raw]+', 'options=[raw,seed,raw15]+')
runtime=runtime.replace("'selected_raw_control':Path(best['directory'])==control,",
    "'selected_raw_control':Path(best['directory']) in {control,seed_dir,raw15_dir},\n              'selected_seed_control':Path(best['directory'])==seed_dir,")
runtime=runtime.replace("print(trial.get('error','No error text saved'),flush=True)",
    "print(trial.get('error','No error text saved'),flush=True)\n        else:\n            print(f\"ACCEPTED: search MAP@12={100*trial['score']:.6f}%\",flush=True)\n        if len(trials)>=config.get('abort_if_no_success_after_calls',6) and not seen:\n            raise RuntimeError('Pilot gate: no successfully measured LLM programs; stopping before spending300 calls')")
runtime=runtime.replace("choices={'Raw LightGBM':out/'raw_control',winner_name:Path(selected['directory'])}",
    "choices={'Raw15 LightGBM':out/'raw15_control','Raw LightGBM':out/'raw_control','Seeded32 LightGBM':out/'seed_control',winner_name:Path(selected['directory'])}")
runtime=runtime.replace("winner_name='Search winner: raw control (NO LLM features)' if selected['selected_raw_control'] else 'LLM-FE LightGBM'",
    "winner_name='Search winner: host control (NO LLM features)' if selected['selected_raw_control'] else 'LLM-FE flat LightGBM'")
runtime=runtime.replace('LLM minus raw AP','LLM minus prepared30 AP').replace("['LLM better','Tie','Raw better']","['Winner better','Tie','Prepared30 better']")
runtime=runtime.replace('Raw LightGBM','Prepared30 LightGBM')
runtime=runtime.replace("'paper_reproduction':False}","'paper_reproduction':False,'base_feature_origin':'15raw+15human historical aggregates','seed_control_origin':'2human log transforms'}")
runtime=runtime.replace("'Adaptation of LLM-FE; not a numerical reproduction of the paper. All MAP values in percent.',",
    "'Flat-table adaptation:15 raw fields+15 human historical aggregates;2 manual seed transforms. Not all features are LLM-generated. All MAP values in percent.',")
assets={'worker.py':worker,'runtime.py':runtime,'flat_features.py':(D/'flat_features.py').read_text(encoding='utf-8'),
        'original_data.py':history_data,'program_guard.py':guard,
        'sql_features.py':(HERE/'sql_variant/sql_features.py').read_text(encoding='utf-8'),
        'archive_helper.py':(HERE/'balance_diagnostic/host.py').read_text(encoding='utf-8')}
for name,source in assets.items():ast.parse(source);(D/name).write_text(source,encoding='utf-8')
for c in base['cells']:
    text=''.join(c['source'])
    if c['cell_type']=='code' and 'MODULES = ' in text:
        a=text.index('MODULES = ');b=text.index('CODE = ',a)
        text=text[:a]+'MODULES = '+repr(assets)+'\n'+text[b:]
    text=text.replace('hm_llmfe_llama31_8b_lightgbm_preflight_fulltrain_v5','hm_llmfe_llama31_8b_lightgbm_flat_fulltrain_v1')
    text=text.replace("MODEL_SOURCE = 'unsloth'", "MODEL_SOURCE = 'hf'")
    text=text.replace("MODEL_REVISION = ''", "MODEL_REVISION = '0e9e39f249a16976918f6564b8830bc894c89659' if MODEL_SOURCE=='hf' else ''")
    text=text.replace("'program_interface_version':5", "'program_interface_version':1,'feature_interface':'flat_python','abort_if_no_success_after_calls':6")
    text=text.replace("WORK / 'llmfe_runtime'", "WORK / 'llmfe_flat_runtime'")
    text=text.replace("'sentencepiece==0.2.1'", "'sentencepiece==0.2.1','duckdb==1.4.1'")
    text=text.replace("'lightgbm','pandas','numpy','pyarrow'", "'lightgbm','pandas','numpy','pyarrow','duckdb'")
    text=text.replace('Raw LightGBM search MAP','Prepared30 LightGBM search MAP')
    if c['cell_type']=='code' and "print('Data checksums: OK')" in text:
        text+='''\nfrom flat_features import prepare
SOURCE_DATA=DATA
DATA,flat_manifest=prepare(SOURCE_DATA,WORK)
CONFIG['flat_manifest_sha256']=hashlib.sha256((DATA/'flat_manifest.json').read_bytes()).hexdigest()
CONFIG['base_feature_origin']='15raw+15human historical aggregates'
print('Prepared flat fields:',flat_manifest['base_fields'])
'''
        before="DATA,flat_manifest=prepare(SOURCE_DATA,WORK)"
        text=text.replace(before,"try:\n    DATA,flat_manifest=prepare(SOURCE_DATA,WORK)\nexcept Exception as error:\n    from archive_helper import pack_results,write_json\n    failed=WORK/('hm_flat_preparation_failed_'+str(time.time_ns()));failed.mkdir()\n    write_json(failed/'config.json',CONFIG)\n    display(FileLink(pack_results(failed,error,stage='table_preparation')))\n    raise")
    if c['cell_type']=='code' and '# Контроль без LLM-признаков' in text:
        text=text.replace("# Контроль без LLM-признаков: реальное обучение на всех803377 парах.","# Prepared30 control, no LLM transformations.")
        text+='''\nfrom flat_features import SEED, RAW_ONLY
for name,code in [('seed_control',SEED),('raw15_control',RAW_ONLY)]:
    directory=OUT/name;directory.mkdir(exist_ok=True)
    (directory/'program.py').write_text(code)
    print(name,experiment.evaluate(DATA,directory,'search',CONFIG)['map'],flush=True)
'''
    if c['cell_type']=='code' and 'selected = experiment.search' in text:
        text=text.replace('selected = experiment.search(DATA, OUT, CONFIG, generate_program)',
            "try:\n    selected = experiment.search(DATA, OUT, CONFIG, generate_program)\nexcept Exception as error:\n    from archive_helper import pack_results\n    display(FileLink(pack_results(OUT,error,stage='search')))\n    raise")
    if c['cell_type']=='code' and ('# Prepared30 control' in text or 'from transformers import AutoTokenizer' in text or 'report = experiment.final' in text):
        text='try:\n'+textwrap.indent(text,'    ')+"except Exception as error:\n    from archive_helper import pack_results\n    display(FileLink(pack_results(OUT,error,stage='controls_model_or_final')))\n    raise\n"
    if c['cell_type']=='markdown':
        text=text.replace('Llama создаёт Python-программы признаков','Llama преобразует готовую плоскую таблицу30 столбцов одной Python-функцией')
        text=text.replace('Короткая Python/pandas-функция,2–6 новых признаков','modify_features(X): готовая таблица, без history/SQL/joins')
        text=text.replace('новый протокол v5','новый протокол flat v1')
        text=text.replace('без старых ручных/GNN-признаков','15 фиксированных исторических агрегатов host; без GNN')
    if c['cell_type']=='code':ast.parse(text)
    c['source']=text.splitlines(keepends=True);c['id']=hashlib.sha256(text.encode()).hexdigest()[:12]
base['cells'][0]['source'].insert(0,'# Новый эксперимент: готовая таблица → Python-преобразования Llama → LightGBM\n\n')
base['cells'][0]['source'].append('\nКонтроли: Raw15, Prepared30 (15raw+15 ручных исторических агрегатов), Seeded32 (ещё2 ручных log-признака). '
    'LLM-поиск сравнивается с этими контролями; начальный пример уже обучен и измерен. '
    'Первые6 обращений — пилот: при0 успешных наборов остановка с ZIP; иначе поиск20/300/3 продолжается. '
    'Подготовленная таблица кэшируется в working; исходный Input-архив прежний.\n')
path=HERE/'llmfe_llama31_hm_flat_kaggle_t4.ipynb'
path.write_text(json.dumps(base,ensure_ascii=False,indent=1),encoding='utf-8')
(D/'delivery_manifest.json').write_text(json.dumps({'notebook':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
    'protocol':'hm_llmfe_llama31_8b_lightgbm_flat_fulltrain_v1','gpu_or_llama_executed':False},indent=2)+'\n')
print('Built',path.name,len(base['cells']),'cells')
