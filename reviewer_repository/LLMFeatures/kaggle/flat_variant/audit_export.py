"""Audit completed user flat-table run and replay frozen models; do not retrain."""
import hashlib
import json
from pathlib import Path
import zipfile
import numpy as np
import pandas as pd
from runtime import evaluate,write_json
from worker import map_at_12

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
ARCHIVE=ROOT/'hm_llmfe_llama31_8b_lightgbm_flat_fulltrain_v1_aa1ed17300ae_results.zip'
OUT=ROOT/'reports/hm_llmfe_flat_v1_audit'
OUT.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(ARCHIVE) as z:
    config=json.loads(z.read('run_config.json'));trials=json.loads(z.read('trials.json'))
    selected=json.loads(z.read('selected.json'));report=json.loads(z.read('report.json'))
    hashes={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()==value for name,value in config['runtime_sha256'].items()}
    assert all(hashes.values()),hashes
    fingerprint=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()[:12]
    assert fingerprint=='aa1ed17300ae',fingerprint
    exported=OUT/'export';exported.mkdir(exist_ok=True)
    for name in z.namelist():
        path=exported/name
        if not path.resolve().is_relative_to(exported.resolve()):raise ValueError('Unsafe zip path')
        if name.endswith('/'):continue
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(z.read(name))
    chosen=Path(selected['directory']).name
    assert chosen=='candidate_003' and not selected['selected_raw_control']
    models={'Raw15 LightGBM':'raw15_control','Prepared30 LightGBM':'raw_control',
            'Seeded32 LightGBM':'seed_control','LLM-FE flat LightGBM':'candidates/'+chosen}
    source=ROOT/'data/kaggle_hm_llmfe_fulltrain_v2'
    assert hashlib.sha256((source/'manifest.json').read_bytes()).hexdigest()==config['bundle_manifest_sha256']
    data_candidates=list((ROOT/'reports/kaggle_llmfe_validation/flat_v1/prepared').glob('hm_flat_table_v1_*'))
    data=next(p for p in data_candidates if (p/'flat_manifest.json').exists())
    flat=json.loads((data/'flat_manifest.json').read_text())
    assert flat['identity']['source_manifest_sha256']==config['bundle_manifest_sha256']
    assert len(flat['base_fields'])==30
    for split in ['train','search','confirm','val','test']:
        old=pd.read_parquet(source/f'{split}_pairs.parquet')
        prepared=pd.read_parquet(data/f'{split}_pairs.parquet')
        pd.testing.assert_frame_equal(prepared[old.columns],old)
    candidate_checks=[]
    for trial in trials:
        if trial['status']!='valid':continue
        folder=exported/'candidates'/f"candidate_{trial['sample']:03d}"
        metrics=json.loads((folder/'search_metrics.json').read_text())
        schema=json.loads((folder/'schema.json').read_text())
        assert schema['train_pairs']==803377 and metrics['map']==trial['score']
        assert hashlib.sha256((folder/'program.py').read_bytes()).hexdigest()==metrics['program_sha256']
        assert hashlib.sha256((folder/'model.txt').read_bytes()).hexdigest()==metrics['model_sha256']
        candidate_checks.append(trial['sample'])
    assert len(candidate_checks)==20
    aps={'val':{},'test':{}}; replay_results=[]
    for label,relative in models.items():
        folder=exported/relative
        for split in ['val','test']:
            truth=pd.read_parquet(source/f'{split}_targets.parquet')
            predictions=np.load(folder/f'{split}_predictions.npy')
            metric,ap=map_at_12(predictions,truth.article_id)
            saved=json.loads((folder/f'{split}_metrics.json').read_text())
            assert saved['map']==metric and np.array_equal(ap,np.load(folder/f'{split}_user_ap.npy'))
            assert metric==report['metrics'][label][split]['map']
            aps[split][label]=ap
            replay=OUT/'independent_frozen_replay'/relative;replay.mkdir(parents=True,exist_ok=True)
            for name in ['program.py','model.txt','schema.json',f'{split}_predictions.npy',f'{split}_user_ap.npy']:
                (replay/name).write_bytes((folder/name).read_bytes())
            result=evaluate(data,replay,'replay_'+split,config)
            assert result['passed'] and result['map']==metric
            replay_results.append({'model':label,'split':split,'map':metric,'exact_replay':True})
            print('Frozen replay passed:',label,split,metric,flush=True)
    for label,key in [('Manual features → LightGBM','manual_lightgbm'),('GNN → LightGBM','gnn_lightgbm'),('ID-GNN (graph training budget)','idgnn')]:
        for split in ['val','test']:
            truth=pd.read_parquet(source/f'{split}_targets.parquet')
            value,ap=map_at_12(np.load(source/f'{split}_{key}_reference.npy'),truth.article_id)
            assert value==report['metrics'][label][split]['map']
            aps[split][label]=ap
    rng=np.random.default_rng(42);boot={}
    winner='LLM-FE flat LightGBM'
    for label in aps['test']:
        if label==winner:continue
        delta=aps['test'][winner]-aps['test'][label]
        means=[]
        for _ in range(40):
            rows=rng.integers(0,len(delta),size=(250,len(delta)))
            means.extend(delta[rows].mean(axis=1))
        ci=np.quantile(means,[.025,.975])
        boot[label]={'mean_delta_pp':float(100*delta.mean()),'paired_bootstrap95_pp':(100*ci).tolist(),
            'better_users':int((delta>0).sum()),'tied_users':int((delta==0).sum()),'worse_users':int((delta<0).sum()),
            'resamples':10000,'exploratory_only':True}
    comparison=pd.read_csv(exported/'comparison.csv')
    lines=['# Проверенный реальный H&M flat-table эксперимент','',
        '20 оценённых программ /23 обращения,3 отказа,3 исправления. Выбран candidate_003 по confirmation512.',
        'Одинаковые803377 train пар; val1024/test2048 пользователей и общие кандидаты ID-GNN.','',
        '| Модель | Val MAP@12, % | Test MAP@12, % |','|---|---:|---:|']
    lines.extend(f'| {r.model} | {100*r.val_map:.5f} | {100*r.test_map:.5f} |' for r in comparison.itertuples())
    lines+=['',
        'Все20 обученных кандидатов проверены по program/model hashes и train_pairs. Конфиг fingerprint и7 runtimeSHA совпадают.',
        'Независимый повтор из сохранённых деревьев:4 модели×val/test, точное совпадение top12/AP/MAP.',
        'Три референса пересчитаны из исходных top12 на тех же пользователях.',
        'Оригинальный ZIP не изменён. Экспортированные файлы: export/. Повторные проверки: independent_frozen_replay/.',
        'flat_manifest отсутствует в ZIP; byte-level сравнение Kaggle-кэша невозможно. Локальные подготовленные',
        'данные восстановлены тем же кодом/исходным bundle; совпадение всех предсказаний проверено.',
        '',
        'Прирост LLM к Prepared30 на test небольшой; см. парный exploratory bootstrap ниже.',
        '95% интервал к Prepared30 и Seeded32 положителен на этой выборке; к Raw15 включает0.',
        'На val Raw15 выше выбранной LLM-модели. Поиск256/confirmation512 дают шумный отбор,',
        'но причина разницы не установлена отдельным экспериментом. Не выбирать новую программу по этому test.',
        '',
        'Выбранные36 полей:15 raw+15 ручных агрегатов+2 ручных seed log+4 новых LLM отношения.',
        'Один purchase ratio делит180-дневное user-article count на30-дневное article count: это не доля одного окна.',
        'Recency ratios защищены проверкой counts, а не знаменателя recency; inf преобразуется вNaN evaluator.',
        'Это допустимый код, но семантические ограничения остаются; выигрыш в исполнении не означает сильных признаков.',
        '',
        '| Сравнение test: LLM минус контроль | Разница, п.п. | 95% парный bootstrap, п.п. |','|---|---:|---|']
    for label,b in boot.items():
        lo,hi=b['paired_bootstrap95_pp'];lines.append(f"| {label} | {b['mean_delta_pp']:+.5f} | [{lo:+.5f}; {hi:+.5f}] |")
    lines+=['','Bootstrap:10000 перевыборок пользователей,seed42; exploratory, не оценка эффекта всех random seeds.',
        'Не весь каталог/не полный test, не воспроизведение статьи. ID-GNN имеет иной upstream-бюджет.',
        '', '![Сравнение](export/comparison.png)','![Поиск](export/search_progress.png)','![AP](export/ap_histograms.png)']
    (OUT/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    write_json(OUT/'audit.json',{'archive_sha256':hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
        'config_fingerprint_matches':True,'runtime_hashes_match':hashes,'validated_candidate_models':candidate_checks,
        'same_original_pair_rows_labels_order':True,'independent_frozen_replays':replay_results,
        'paired_test_bootstrap':boot,'comparison':comparison.to_dict('records'),
        'full_catalog':False,'real_llama_results':True,'paper_reproduction':False})
    print(json.dumps({'report':str(OUT/'report.md'),'bootstrap':boot},ensure_ascii=False,indent=2),flush=True)
