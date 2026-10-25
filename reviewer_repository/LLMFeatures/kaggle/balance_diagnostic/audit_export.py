"""Read-only audit of the user's completed Kaggle diagnostic; bounded CPU re-evaluation."""
import ast
import hashlib
import json
from pathlib import Path
import textwrap
import zipfile
from host import evaluate,write_json
from worker import extract

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
ARCHIVE=HERE.parent/'balance_scale_llama31_diagnostic_v2_cpu_6b5c7786f4b5_results.zip'
OUT=ROOT/'reports/balance_scale_llama31_diagnostic_v2_audit'
OUT.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(ARCHIVE) as archive:
    config=json.loads(archive.read('run_config.json'))
    trials=json.loads(archive.read('trials.json'))
    summary=json.loads(archive.read('summary.json'))
    modules={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()==value for name,value in config['runtime_sha256'].items()}
    assert all(modules.values()),modules
    assert hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()[:12]=='6b5c7786f4b5'
    for name in archive.namelist():
        destination=OUT/'export'/name
        if not destination.resolve().is_relative_to((OUT/'export').resolve()):raise ValueError('Unsafe zip path')
        if name.endswith('/'):continue
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(archive.read(name))
    replays=[];completion_checks=[]
    for trial in trials:
        stem=f"{trial['format']}_seed{trial['seed']}"
        response=json.loads(archive.read(stem+'/response.json'))
        if trial['format']=='chat':
            source=extract(response['text'])
            assert source==archive.read(stem+'/program.py').decode()
            directory=OUT/'independent_cpu_replay'/stem;directory.mkdir(parents=True,exist_ok=True)
            (directory/'response.txt').write_text(response['text'])
            replay=evaluate(HERE/'upstream',directory)
            assert replay['status']=='valid',replay
            assert replay['cv_folds']==trial['cv_folds'],(stem,replay['cv_folds'],trial['cv_folds'])
            replays.append({'sample':stem,'cv_accuracy':replay['cv_accuracy'],'exact_fold_scores_match':True})
        else:
            # Static check ONLY: distinguish stopping failures from inability to start a function.
            prefix=response['text'].split('\ndef modify_features_v2',1)[0]
            try:
                tree=ast.parse('def modify_features(df_input):\n'+textwrap.indent(textwrap.dedent(prefix).strip(),'    '))
                complete=any(isinstance(n,ast.Return) for n in ast.walk(tree))
            except SyntaxError:complete=False
            completion_checks.append({'sample':stem,'first_function_prefix_parses_and_has_return':complete,
                'not_evaluated':True,'original_status':trial['status'],'original_truncated':trial['truncated']})
    raw=summary['controls']['raw']['cv_accuracy']
    rows=[('Raw control',raw),('Authors seed',summary['controls']['authors_seed']['cv_accuracy'])]
    rows.extend((f"Llama chat seed{t['seed']}",t['cv_accuracy']) for t in trials if t['format']=='chat')
    lines=['# Реальная диагностика Llama на balance-scale','',
        'Официальная Llama-3.1-8B-Instruct, NF4/double quant/FP16, T4, revision '+config['model_revision']+'.','',
        '| Вариант | 4-fold train CV accuracy |','|---|---:|']
    lines.extend(f'| {name} | {100*value:.1f}% |' for name,value in rows)
    lines+=['',
        'Chat:3/3 исполнимых ответа, два лучше raw. Независимый CPU replay всех трёх точно совпал по4 fold scores.',
        'Completion:0/3 принятых; все3 достигли2048 токенов. Начальные тела функций синтаксически завершены,',
        'но затем модель генерирует следующие версии/повторы. Нельзя приравнивать это к отсутствию исполнимого кода.',
        'Статические prefix checks не являются новой оценкой и не меняют исходные статусы.',
        '',
        'Seed44 использует произведения вес×плечо для обеих сторон; физически осмысленные признаки.',
        'Есть неточные названия: weight_ratio/distance_ratio фактически средние; seed43 содержит дублирующие формулы.',
        'Seed42 удаляет исходные поля и получает81.4%, ниже raw87.0%. Исполнимость не гарантирует улучшения.',
        '',
        'Это500 train строк,4-fold CV;125 heldout не открывались.96.8% не test accuracy и не результат H&M.',
        'Три ответа не доказывают универсальную надёжность или отсутствие эффекта квантизации.',
        'H&M уже использовал chat template: неудачу H&M нельзя объяснить отсутствием chat template.',
        'Поддерживаемая гипотеза: текущая Llama способна генерировать признаки для знакомого Python-интерфейса',
        'с конкретным работающим примером; custom DSL/relational постановка остаются неподтверждённой адаптацией.',
        '',
        'Оригинальный ZIP не изменён; копия экспортированных файлов: export/. Replay: independent_cpu_replay/.']
    (OUT/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    write_json(OUT/'audit.json',{'archive_sha256':hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
        'config_fingerprint_matches':True,'runtime_hash_matches':modules,'real_llama_output':True,
        'chat_valid':3,'chat_calls':3,'completion_truncated':3,'completion_calls':3,
        'chat_improved_vs_raw':sum(t['cv_accuracy']>raw for t in trials if t['format']=='chat'),
        'independent_replays':replays,'completion_static_checks':completion_checks,
        'heldout_evaluated':False,'h_and_m_evaluated':False,'paper_reproduction':False})
print(json.dumps({'report':str(OUT/'report.md'),'replayed':replays,'completion_static':completion_checks},indent=2))
