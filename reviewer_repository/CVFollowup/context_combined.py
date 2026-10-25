"""Categorical article codes + fanout64/32, isolated three-fold validation run."""
import argparse
import gc
import inspect
import json
from pathlib import Path
import shutil
import sys

import context_first3 as base
from common import ROOT, OUT, REPORT, read, write, sha, record

RUN='hm_medium_context_combined_seed42_v1'
DEST=OUT/'context_combined_v1'
REP=REPORT/'context_combined_v1'
PREVIOUS=OUT/'context_first3_v1'


def freeze_protocol():
    REP.mkdir(parents=True,exist_ok=True)
    previous_manifest=read(REPORT/'context_first3_v1/source_manifest.json')
    assert sha(Path(base.__file__))==previous_manifest['CVFollowup/context_first3.py']
    manifest={}
    for fold in range(3):
        for arm in ['categorical','fanout64']:
            folder=PREVIOUS/f'fold_{fold}'/arm
            result=read(folder/'result.json')
            assert sha(folder/'best.pt')==result['checkpoint_sha256']
            for name in ['best.pt','result.json','val_ap.npy']:
                path=folder/name
                manifest[str(path.relative_to(ROOT))]=sha(path)
        folder=OUT/f'fold_{fold}/gnn_timefix_refit/contextgnn'
        for name in ['best.pt','val_predictions.npy','val_scores.npy']:
            path=folder/name
            manifest[str(path.relative_to(ROOT))]=sha(path)
        path=ROOT/f'data/hm-cv-medium-v2/fold_{fold}/subset_manifest.json'
        manifest[str(path.relative_to(ROOT))]=sha(path)
    protocol=dict(run_id=RUN,validation_only=True,seed=42,folds=[0,1,2],fanout=[64,32],
        categorical_columns=base.CODE_COLUMNS,gate=False,loss='original full-catalog sparse CE',
        optimizer='Adam lr=.001',batch_size=128,max_epochs=10,patience=3,
        selection='Original fixed 256 search-validation rows per fold; no test evaluation',
        comparisons=['original','fanout64','categorical','combined'],
        note='Exploratory on repeatedly used checkpoint-selection validation; one seed.',
        reference_hashes=manifest,
        sources={str(Path(__file__).relative_to(ROOT)):sha(Path(__file__)),
                 str(Path(base.__file__).relative_to(ROOT)):sha(Path(base.__file__))})
    path=REP/'protocol.json'
    if path.exists():
        assert read(path)==protocol,'Protocol changed: use a new run ID'
    else:
        write(path,protocol)
    # Preserve exact executed source, including the reused training implementation.
    for name in ['context_combined.py','context_first3.py']:
        dest=REP/name
        source=ROOT/'CVFollowup'/name
        if dest.exists():
            assert sha(dest)==sha(source)
        else:
            shutil.copyfile(source,dest)
    return protocol


def train():
    import fcntl
    protocol=freeze_protocol()
    base.RUN,base.DEST,base.REP=RUN,DEST,REP
    source=inspect.getsource(base.refit)
    assert source.count("arm == 'categorical'")==1
    assert source.count("arm=='categorical'")==1
    assert source.count("arm == 'fanout64'")==1
    source=source.replace("arm == 'categorical'","arm in ('categorical','combined')")
    source=source.replace("arm=='categorical'","arm in ('categorical','combined')")
    source=source.replace("arm == 'fanout64'","arm in ('fanout64','combined')")
    path=REP/'refit_runtime.py'
    if path.exists():
        assert path.read_text(encoding='utf-8')==source
    else:
        path.write_text(source,encoding='utf-8')
    exec(compile(source,str(path),'exec'),base.__dict__)
    DEST.mkdir(parents=True,exist_ok=True)
    with (DEST/'execution.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        record('context_combined_started','Authorized categorical article codes plus fanout64/32, three folds, original training settings and validation only. H010 CPU/API left untouched.',RUN,status='training',artifacts=str(REP.relative_to(ROOT)))
        for fold in range(3):
            work=DEST/f'fold_{fold}/combined'
            if (work/'result.json').exists():
                result=read(work/'result.json')
                assert sha(work/'best.pt')==result['checkpoint_sha256']
                print('REUSE',fold,flush=True)
                continue
            if (work/'history.json').exists():
                raise RuntimeError(f'Partial fit {work}: preserve before restarting, no silent overwrite')
            (DEST/f'fold_{fold}/diagnostic').mkdir(parents=True,exist_ok=True)
            base.refit(fold,'combined')
            result=read(work/'result.json')
            assert result['fanout']==[64,32]
            assert result['changed_columns']==base.CODE_COLUMNS
            schema=result['materialized_schema']['article']
            categorical={c for kind,columns in schema.items() if kind.split('.')[-1]=='categorical' for c in columns}
            assert set(base.CODE_COLUMNS)<=categorical
            result['protocol_sha256']=sha(REP/'protocol.json')
            result['executed_refit_sha256']=sha(path)
            result['wrapper_sha256']=sha(Path(__file__))
            write(work/'result.json',result)
        record('context_combined_trained','Three combined ContextGNN fits finished with checkpoint reload and independent validation AP verification; comparison report pending.',RUN,status='validation_verified_pending_report')
    summarize()


def summarize():
    import numpy as np
    protocol=read(REP/'protocol.json')
    for path,digest in protocol['reference_hashes'].items():
        assert sha(ROOT/path)==digest,f'Reference changed: {path}'
    arrays={name:[] for name in ['original','fanout64','categorical','combined']}
    fits=[]
    for fold in range(3):
        diagnostic=PREVIOUS/f'fold_{fold}/diagnostic'
        arrays['original'].append(np.load(diagnostic/'32_16_original_ap.npy'))
        for name in ['fanout64','categorical']:
            arrays[name].append(np.load(PREVIOUS/f'fold_{fold}'/name/'val_ap.npy'))
        folder=DEST/f'fold_{fold}/combined'
        fit=read(folder/'result.json')
        assert sha(folder/'best.pt')==fit['checkpoint_sha256']
        fits.append(fit)
        arrays['combined'].append(np.load(folder/'val_ap.npy'))
        assert np.array_equal(np.load(diagnostic/'val_customer_ids.npy'),
                              np.load(DEST/f'fold_{fold}/diagnostic/val_customer_ids.npy'))
    customers=np.concatenate([np.load(PREVIOUS/f'fold_{f}/diagnostic/val_customer_ids.npy') for f in range(3)])
    unique,inverse=np.unique(customers,return_inverse=True)
    counts=np.bincount(inverse)
    pooled={name:np.concatenate(value) for name,value in arrays.items()}
    metrics={name:dict(fold_map=[float(a.mean()) for a in value],pooled_map=float(pooled[name].mean())) for name,value in arrays.items()}
    differences={name:pooled['combined']-pooled[name] for name in ['original','fanout64','categorical']}
    differences['interaction']=pooled['combined']-pooled['fanout64']-pooled['categorical']+pooled['original']
    intervals={}
    for name,delta in differences.items():
        sums=np.bincount(inverse,weights=delta)
        rng=np.random.default_rng(42)
        boot=[]
        for _ in range(5000):
            ix=rng.integers(0,len(unique),len(unique))
            boot.append(sums[ix].sum()/counts[ix].sum())
        intervals[name]=dict(delta=float(delta.mean()),ci95=list(map(float,np.quantile(boot,[.025,.975]))),
            fold_delta=[float(delta[i*256:(i+1)*256].mean()) for i in range(3)])
    summary=dict(run_id=RUN,validation_only=True,observations=len(customers),customers=len(unique),
        metrics=metrics,differences=intervals,fits=fits,reference_hashes_unchanged=True,
        note='5000 paired customer bootstrap; exploratory selection validation, one seed; no test evaluation.')
    write(REP/'comparison.json',summary)
    names={'original':'Исходный ContextGNN','fanout64':'Только fanout64/32','categorical':'Только категориальные коды','combined':'Fanout64/32 + категориальные коды'}
    lines=['# ContextGNN: совместное изменение fanout и типов признаков','',
        '2026-10-18. Три новых обучения, seed42. Только прежняя search-validation: '
        '256 наблюдений на фолд, всего768/753покупателя. Test не оценивался.','',
        '| Вариант | Fold0 MAP,% | Fold1 MAP,% | Fold2 MAP,% | Pooled MAP,% |',
        '|---|---:|---:|---:|---:|']
    for name,value in metrics.items():
        lines.append('| '+names[name]+' | '+' | '.join(f'{100*x:.4f}' for x in value['fold_map'])+f" | {100*value['pooled_map']:.4f} |")
    lines+=['','| Разница | Среднее, п.п. | Парный95%интервал, п.п. |','|---|---:|---:|']
    for name,value in intervals.items():
        label='Взаимодействие: combined−fanout−categorical+original' if name=='interaction' else 'Сочетание минус '+names[name]
        lo,hi=value['ci95']
        lines.append(f"| {label} | {100*value['delta']:+.4f} | [{100*lo:+.4f}; {100*hi:+.4f}] |")
    lines+=['','Интервалы:5000 парных bootstrap по покупателю с сохранением всех его '
        'наблюдений. Условны на этих моделях и неоднократно использованной validation '
        'выбора эпохи; не учитывают новые seeds/недели и оптимизм отбора, без поправки '
        'на множество сравнений. Взаимодействие — описательная разность на шкале AP.', '',
        'Меняются совместно только fanout32/16→64/32 и типы восьми кодов товара '
        'numerical→categorical. Прежние sparse CE, Adam lr0.001, batch128, максимум10 '
        'полных эпох, patience3, исходная жёсткая локальная замена; обучаемой смеси нет.', '',
        ', '.join('`'+c+'`' for c in base.CODE_COLUMNS)+'.','',
        'Все модели обучены с нуля в отдельных каталогах и кэшах. Проверены фактическая '
        'схема и fanout, отсутствие будущих временных узлов, независимый AP, перезагрузка '
        'выбранных весов с точным AP и ранее установленным FP32-допуском скоров. '
        'Хеши прежних моделей, предсказаний, AP и манифестов данных совпали после обучения.', '',
        '## Выбранные эпохи','', '| Фолд | Лучшая эпоха | Завершено эпох |', '|---|---:|---:|']
    for fit in fits:
        lines.append(f"| {fit['fold']} | {fit['best_epoch']} | {fit['epochs']} |")
    lines+=['','Результаты и веса: `CVFollowup/results/v1/context_combined_v1/`. '
        'Протокол и контрольные суммы до запуска: `protocol.json`; численные результаты: '
        '`comparison.json`; точная реализация обучения: `refit_runtime.py`.','']
    (REP/'report_ru.md').write_text('\n'.join(lines),encoding='utf-8')
    record('context_combined_complete','Combined categorical codes plus fanout64/32 evaluated on all three validation folds; independent AP/checkpoint reload verified; reference hashes unchanged. No test evaluation.',RUN,status='complete_validation_comparison',artifacts=str((REP/'report_ru.md').relative_to(ROOT)),pooled_validation=metrics,differences=intervals)
    print(json.dumps(summary['metrics'],indent=2),flush=True)
    print(json.dumps(intervals,indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('stage',choices=['train','summary'],default='train',nargs='?')
    args=parser.parse_args()
    if args.stage=='train':
        train()
    else:
        summarize()
