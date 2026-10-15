"""Read-only audit of an exported Kaggle notebook; never executes supplied Python."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'hm_llmfe_llama31_8b_lightgbm_fulltrain_v3_3b338cf1f141_results'
DEST=ROOT/'reports/kaggle_llama_v3_audit'


def main():
    DEST.mkdir(parents=True,exist_ok=True)
    config=json.loads((SOURCE/'run_config.json').read_text())
    notebook=json.loads((SOURCE/'features-llama-plus-lightgbm.ipynb').read_text())
    embedded={}
    for cell in notebook['cells']:
        if cell['cell_type']!='code':
            continue
        try:
            tree=ast.parse(''.join(cell['source']))
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MODULES' for t in node.targets):
                embedded=ast.literal_eval(node.value)
    hashes={name:hashlib.sha256(text.encode()).hexdigest() for name,text in embedded.items()}
    assert hashes==config['runtime_sha256']
    trials=[]
    for file in sorted(SOURCE.glob('candidates/*/trial.json')):
        trial=json.loads(file.read_text())
        response=json.loads((file.parent/'response.json').read_text())
        error=trial.get('error','')
        last=error.splitlines()[-1] if error else ''
        if response.get('truncated'):
            category='truncated'
        elif 'No imports/classes' in error:
            category='interface_import'
        elif 'KeyError' in error:
            category='missing_column'
        elif 'unchanged X.index' in error or 'duplicate labels' in error:
            category='row_index'
        else:
            category='other_pandas_runtime'
        source=(file.parent/'program.py').read_text() if (file.parent/'program.py').exists() else None
        trace_lines=[int(n) for n in re.findall(r'File "<llm-features>", line (\d+)',error)]
        snippets=[]
        if source:
            lines=source.splitlines()
            for number in trace_lines:
                snippets.append({'line':number,'context':'\n'.join(f'{i+1}: {lines[i]}' for i in range(max(0,number-3),min(len(lines),number+2)))})
        trials.append({'candidate':trial['sample'],'island':trial['island'],'category':category,
                       'error':last,'full_error':error,'source_context':snippets,
                       'generated_tokens':response.get('generated_tokens'),'truncated':response.get('truncated',False),
                       'seconds':trial['elapsed_seconds'],'model_created':(file.parent/'model.txt').exists(),
                       'has_search_metrics':(file.parent/'search_metrics.json').exists(),
                       'returns_X':bool(source and re.search(r'\breturn\s+X\s*$',source,re.M))})
    counts=dict(Counter(t['category'] for t in trials))
    selected=json.loads((SOURCE/'selected.json').read_text())
    report={'source_directory':str(SOURCE.relative_to(ROOT)),'protocol':config['protocol'],
            'runtime_hashes_match_exported_notebook':True,'calls':len(trials),'valid':0,
            'categories':counts,'total_candidate_seconds':sum(t['seconds'] for t in trials),
            'models_created':sum(t['model_created'] for t in trials),
            'search_metrics_created':sum(t['has_search_metrics'] for t in trials),
            'selected_raw_control':selected['selected_raw_control'],
            'llm_quality_measured':False,'trials':trials}
    import numpy as np
    import pandas as pd
    from worker import map_at_12
    data=ROOT/'data/kaggle_hm_llmfe_fulltrain_v2'
    assert hashlib.sha256((data/'manifest.json').read_bytes()).hexdigest()==config['bundle_manifest_sha256']
    comparison=pd.read_csv(SOURCE/'comparison.csv')
    checked={}
    for split in ['val','test']:
        targets=pd.read_parquet(data/f'{split}_targets.parquet')
        predictions=np.load(SOURCE/f'raw_control/{split}_predictions.npy')
        value,_=map_at_12(predictions,targets.article_id)
        expected=float(comparison.loc[comparison.model=='Raw LightGBM',split+'_map'].iloc[0])
        assert abs(value-expected)<1e-12
        checked[split]={'raw_control_map':value,'users':len(targets),'predictions_recomputed':True}
    report['raw_control_verification']=checked
    report['data_bundle_manifest_matches']=True
    assert len(trials)==20 and all(not t['has_search_metrics'] for t in trials)
    (DEST/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# Аудит реального Kaggle-запуска Llama v3','',
           'Это аудит предоставленных артефактов, без нового обучения и без изменения программLLM.',
           f"Версия: {config['protocol']}.20 предложений,0 успешно оценённых, исправлений вv3 нет.",
           'Хеши worker/runtime из вложенного.ipynb точно совпали сrun_config.json.',
           'Все отклонения сохранены; ни одна LLM-модельLightGBM не получила searchMAP.',
           'Выбран raw_control. Строка LLM-FE в исходном отчёте повторяет rawMAP и не является результатомLLM-признаков.',
           '', '| Причина | Число |','|---|---:|']
    lines += [f'| {name} | {count} |' for name,count in counts.items()]
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    labels={'missing_column':'Missing columns','other_pandas_runtime':'Other pandas runtime errors',
            'row_index':'Row/index contract','truncated':'Truncated output','interface_import':'Forbidden imports'}
    fig,ax=plt.subplots(figsize=(9,4))
    bars=ax.barh([labels[k] for k in counts],list(counts.values()))
    ax.bar_label(bars,padding=3)
    ax.set(xlim=(0,max(counts.values())+2),xlabel='Rejected programs',title='Actual Kaggle v3:20 proposals,0 measured LLM programs')
    fig.tight_layout();fig.savefig(DEST/'rejection_categories.png',dpi=150);plt.close(fig)
    lines+=['','![Failure categories](rejection_categories.png)']
    lines += ['',f"Время20 попыток: {report['total_candidate_seconds']/60:.1f}минут; включаетгенерацию/проверку.",
              '', '| Попытка | Популяция | Причина | Токены |','|---|---:|---|---:|']
    lines += [f"| {t['candidate']} | {t['island']} | {t['error'].replace('|','/')} | {t['generated_tokens']} |" for t in trials]
    lines += ['', '## Проверенные примеры',
              '', 'candidate001: history.merge(X,on=customer_id) создаёт article_id_x/article_id_y; последующий groupby(article_id) падает.',
              'До этого агрегаты присоединяются слева кX, а не Xслева кагрегату: возможны неверныепорядок/числострок.',
              'candidate002: past_purchases запрашивается изrecent_transactions, хотя втом столбцы customer_id/article_id/price; также возвращаются имена безf_.',
              'candidate003: groupby().rolling().reset_index() дал3колонки, а код переименовывает ихдвумя именами. rolling(7) —7строк, не7дней.',
              'candidate003 также обращается кraw_u_* вhistory, хотя тамcustomer_age; позже использует отсутствующий X.price.',
              '', '## Выводы для нового ноутбука',
              '', 'Ясно отделитьX отhistory, показать реальныеexamples обоих, сократить генерации до2–6признаков.',
              'Указать сохранениеX.index/однойстрокинапару, many_to_one merge, именаf_, отсутствиеraw_u_*вhistory.',
              'Проверять программу на небольших реальных временных снимках перед803377-парным обучением.',
              'ВозвращатьLLM короткую ошибку с конкретной строкой еёкода и доступнымистолбцами.',
              'Исправить отчёт: rawfallback не подписывать какLLM-признаки.',
              'Эти изменения улучшаютконтракт/диагностику; они не доказываютуспехгенераций без новогофактическогозапуска.']
    (DEST/'report.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='trials'},ensure_ascii=False))


if __name__=='__main__':
    main()
