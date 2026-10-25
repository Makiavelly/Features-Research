"""Frozen-model novelty diagnostics for H010/H011; extend plots in a new report."""
import argparse
import concurrent.futures
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time

for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[name] = '2'
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'CVFollowup'))
import novelty_audit as audit
from common import read, write, sha, record

RUN = 'hm_medium_h010_h011_novelty_seed42_v1'
REPORT = ROOT / 'reports/medium_h010_h011_novelty_v1'
OUT = ROOT / 'LLMResearch/results/novelty_v1'
LABELS = {'h010_20': 'H010: SQL research / 20 sets', 'h011_20': 'H011: autonomous Codex / 20 sets'}


def paths(fold, key):
    if key == 'h010_20':
        folder = ROOT / f'LLMResearch/results/v2/fold_{fold}'
        selected = read(folder / 'gpt61sol_generated_only/selected.json')
    else:
        folder = ROOT / f'LLMResearch/agent_environment/sessions/h011_codex_seed42_v1/fold_{fold}'
        selected = read(folder / 'selected.json')
    source = Path(selected['directory'])
    assert sha(source / 'model.txt') == selected['model_sha256']
    assert sha(source / 'program.json') == selected['program_sha256']
    return folder, source


def protocol():
    assert read(audit.REP / 'final_verification.json')['passed']
    refs = {}
    for fold in range(3):
        for name in ['annotations.json', 'seen_mask.npy']:
            path = audit.DEST / f'fold_{fold}' / name
            refs[str(path.relative_to(ROOT))] = sha(path)
        for key in LABELS:
            folder, source = paths(fold, key)
            assert read(folder / 'verification.json')['passed']
            for path in [source / 'model.txt', source / 'program.json', source / 'feature_schema.json',
                         folder / 'test_predictions.npy', folder / 'test_ap.npy']:
                refs[str(path.relative_to(ROOT))] = sha(path)
    for path in [Path(__file__), ROOT / 'CVFollowup/novelty_audit.py', audit.REP / 'metrics.csv',
                 audit.REP / 'per_user_metrics.parquet']:
        refs[str(path.relative_to(ROOT))] = sha(path)
    value = {'run_id': RUN, 'no_training': True, 'no_api': True, 'no_reselection': True,
             'history_and_metrics': 'Reuse verified original novelty annotations, full source-history masks and per_user/aggregate functions',
             'normal': 'All full-catalog original top12 must reproduce exactly before masking',
             'new_only': 'Mask all previously purchased candidate items before full-catalog top12; not filtering saved top12',
             'references_sha256': refs, 'post_hoc': True}
    REPORT.mkdir(parents=True, exist_ok=True)
    path = REPORT / 'protocol.json'
    if path.exists():
        assert read(path) == value, 'Frozen novelty inputs changed'
    else:
        write(path, value)


def score(fold, key):
    import numpy as np
    import pandas as pd
    import lightgbm as lgb
    folder, source = paths(fold, key)
    dest = OUT / f'fold_{fold}' / key
    dest.mkdir(parents=True, exist_ok=True)
    if (dest / 'verification.json').exists():
        assert read(dest / 'verification.json')['passed']
        return
    runtime = ROOT / f'CVBenchmark/results/medium_v2/fold_{fold}/runtime/api'
    sys.path.insert(0, str(runtime))
    from features import FeatureEngine, validate_program
    from worker import timed_frame
    bundle = ROOT / f'data/hm-cv-medium-v2/fold_{fold}/bundle'
    target = pd.read_parquet(bundle / 'test_targets.parquet')
    masks = np.load(audit.DEST / f'fold_{fold}/seen_mask.npy', mmap_mode='r')
    annotations = read(audit.DEST / f'fold_{fold}/annotations.json')
    expected = np.load(folder / 'test_predictions.npy')
    np.testing.assert_array_equal(target.customer_id, np.load(folder / 'test_users.npy'))
    assert masks.shape == (len(target), 10000)
    assert [a['customer_id'] for a in annotations] == target.customer_id.tolist()
    assert all(a['cutoff'] == str(t) for a, t in zip(annotations, target.timestamp))
    model = lgb.Booster(model_file=str(source / 'model.txt'))
    program = validate_program(read(source / 'program.json'))
    names = model.feature_name()
    assert names == read(source / 'feature_schema.json')['features']
    engine = FeatureEngine(dest / 'scratch', bundle)
    engine.prepare(target.timestamp.iloc[0], target.customer_id.to_numpy(), program)
    engine.names = list(names)
    result = []
    started = time.monotonic()
    try:
        for start in range(0, len(target), 8):
            users = target.customer_id.iloc[start:start + 8].to_numpy()
            pairs = pd.DataFrame({'customer_id': np.repeat(users, 10000),
                                  'article_id': np.tile(np.arange(10000), len(users))})
            scores = model.predict(timed_frame(engine, pairs), num_threads=2).reshape(len(users), 10000)
            assert np.isfinite(scores).all()
            normal = np.argsort(-scores, axis=1, kind='stable')[:, :12]
            np.testing.assert_array_equal(normal, expected[start:start + len(users)])
            scores[masks[start:start + len(users)]] = -np.inf
            novel = np.argsort(-scores, axis=1, kind='stable')[:, :12]
            assert np.isfinite(np.take_along_axis(scores, novel, axis=1)).all()
            assert not masks[start:start + len(users)][np.arange(len(users))[:, None], novel].any()
            result.append(novel)
            if start % 128 == 0:
                progress = {'fold': fold, 'method': key, 'users_done': start + len(users),
                            'users': len(target), 'seconds': time.monotonic() - started}
                write(dest / 'progress.json', progress)
                print(progress, flush=True)
    finally:
        engine.close()
    novel = np.concatenate(result)
    np.save(dest / 'new_predictions.npy', novel)
    write(dest / 'verification.json', {'passed': True, 'normal_top12_identical': True,
          'all_full_catalog_original_predictions_replayed': True, 'no_training': True,
          'no_api': True, 'model_sha256': sha(source / 'model.txt'),
          'program_sha256': sha(source / 'program.json'), 'prediction_sha256': sha(dest / 'new_predictions.npy'),
          'users': len(target), 'seconds': time.monotonic() - started})
    record('h010_h011_novelty_scored', f'{key} fold{fold}: exact original top12 replay passed; unseen-only full-catalog ranking saved.',
           RUN + f'_{key}_fold{fold}', status='verified', artifacts=str(dest.relative_to(ROOT)))


def report():
    import numpy as np
    import pandas as pd
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    rows = []
    for fold in range(3):
        annotations = read(audit.DEST / f'fold_{fold}/annotations.json')
        masks = np.load(audit.DEST / f'fold_{fold}/seen_mask.npy', mmap_mode='r')
        for key, label in LABELS.items():
            folder, _ = paths(fold, key)
            dest = OUT / f'fold_{fold}' / key
            assert read(dest / 'verification.json')['passed']
            for mode, pred in [('normal', np.load(folder / 'test_predictions.npy')),
                               ('new_only', np.load(dest / 'new_predictions.npy'))]:
                for i, (rec, annotation) in enumerate(zip(pred, annotations)):
                    assert len(set(map(int, rec))) == 12
                    if mode == 'new_only':
                        assert not masks[i, rec].any()
                    for group, value in audit.per_user(rec, annotation).items():
                        rows.append(dict(fold=fold, row=i, customer=annotation['original_customer_id'],
                                         method=key, label=label, mode=mode, group=group,
                                         recommendation_count=12, repeat_recommendations=int(masks[i, rec].sum()), **value))
    users = pd.DataFrame(rows)
    for fold in range(3):
        for key in LABELS:
            selected = users[(users.fold == fold) & (users.method == key) &
                             (users['mode'] == 'normal') & (users['group'] == 'all')].sort_values('row')
            folder, _ = paths(fold, key)
            np.testing.assert_allclose(selected['map'], np.load(folder / 'test_ap.npy'), atol=1e-12, rtol=0)
    users.to_parquet(REPORT / 'per_user_metrics.parquet', index=False)
    metrics = users.groupby(['method', 'label', 'mode', 'group'], sort=False).apply(audit.aggregate, include_groups=False).reset_index()
    metrics.to_csv(REPORT / 'metrics_new_methods.csv', index=False)
    users.groupby(['fold', 'method', 'label', 'mode', 'group'], sort=False).apply(audit.aggregate, include_groups=False).reset_index().to_csv(REPORT / 'fold_metrics.csv', index=False)
    combined = pd.concat([pd.read_csv(audit.REP / 'metrics.csv'), metrics], ignore_index=True)
    combined.to_csv(REPORT / 'metrics_all_methods.csv', index=False)
    baseline = pd.read_parquet(audit.REP / 'per_user_metrics.parquet', filters=[('method', '==', 'h009_20'), ('group', '==', 'new')])
    differences = []
    for mode in ['normal', 'new_only']:
        other = baseline[baseline['mode'] == mode].sort_values(['fold', 'row'])
        for key in LABELS:
            own = users[(users.method == key) & (users['mode'] == mode) & (users['group'] == 'new')].sort_values(['fold', 'row'])
            np.testing.assert_array_equal(own[['fold', 'row', 'customer']], other[['fold', 'row', 'customer']])
            for metric in ['recall', 'available_recall']:
                eligible = own[metric].notna().to_numpy()
                np.testing.assert_array_equal(eligible, other[metric].notna())
                delta = own[metric].to_numpy()[eligible] - other[metric].to_numpy()[eligible]
                _, inv = np.unique(own.customer.to_numpy()[eligible], return_inverse=True)
                counts = np.bincount(inv)
                sums = np.bincount(inv, weights=delta)
                rng = np.random.default_rng(42)
                boots = []
                for _ in range(5000):
                    ix = rng.integers(0, len(counts), len(counts))
                    boots.append(sums[ix].sum() / counts[ix].sum())
                low, high = np.quantile(boots, [.025, .975])
                differences.append(dict(method=key, reference='h009_20', mode=mode, metric=metric,
                                        difference=float(delta.mean()), ci95_low=float(low), ci95_high=float(high)))
    pd.DataFrame(differences).to_csv(REPORT / 'paired_recall_differences.csv', index=False)
    normal = combined[(combined['mode'] == 'normal') & (combined['group'] == 'all')].sort_values('map', ascending=False)
    keys, labels = normal.method.tolist(), normal.label.tolist()
    assert len(keys) == len(set(keys)) == 17
    fig, axes = plt.subplots(1, 2, figsize=(19, 12), sharey=True)
    maximum = 0
    for ax, mode, title in zip(axes, ['normal', 'new_only'], ['Обычные рекомендации', 'Ранее купленные товары исключены до top12']):
        part = combined[(combined['mode'] == mode) & (combined['group'] == 'new')].set_index('method').loc[keys]
        values = part.available_macro_recall.to_numpy() * 100
        maximum = max(maximum, values.max())
        ax.barh(range(len(keys)), values, color=[{'h010_20': '#1976d2', 'h011_20': '#7c3aed', 'h009_20': '#ea8c24'}.get(k, '#9aa7b6') for k in keys])
        ax.set(yticks=range(len(keys)), yticklabels=labels, title=title,
               xlabel='Macro Recall@12 доступных новых для покупателя товаров, %')
        for y, value in enumerate(values):
            ax.text(value + .025, y, f'{value:.3f}%', va='center', fontsize=8)
        ax.xaxis.grid(True, alpha=.15)
        ax.set_axisbelow(True)
    axes[0].invert_yaxis()
    for ax in axes:
        ax.set_xlim(0, maximum * 1.16)
    fig.suptitle('Recall новых для покупателя товаров: H010 и H011 среди остальных методов', fontsize=17, y=.98)
    fig.text(.02, .025, 'Те же test-недели и доступные цели; одинаковые пользователи. «Новый» = ранее не покупался этим покупателем.\n'
             'TDM сохраняет beam64; у ID-GNN новые рекомендации — разрешение нулевых ничьих по ID. Нового обучения/API нет.', fontsize=10)
    fig.subplots_adjust(left=.29, right=.98, bottom=.10, top=.93, wspace=.12)
    fig.savefig(REPORT / 'new_item_recall.png', dpi=160)
    fig.savefig(REPORT / 'new_item_recall.svg')
    plt.close(fig)
    new = metrics[metrics['group'] == 'new']
    lines = ['# Recall новых товаров: H010 и H011', '',
             'Метрика и маски повторяют исходный novelty-аудит. Новые товары ранее не покупались данным пользователем; '
             'условная доступная метрика использует только цели в каталоге. Полная метрика сохраняет недоступные цели.', '',
             '| Метод | Режим | Recall всех новых целей | Recall доступных новых целей | Наблюдений с доступными целями |', '|---|---|---:|---:|---:|']
    for r in new.itertuples():
        lines.append(f'|{r.label}|{r.mode}|{r.macro_recall*100:.4f}%|{r.available_macro_recall*100:.4f}%|{int(r.available_users)}|')
    lines += ['', 'Все шесть исходных top12 воспроизведены точно; AP независимо сверены с сохранёнными AP. '
              'В new_only маска применяется к полному каталогу до top12, а не к сохранённому списку. '
              'Обучения, новых API-запросов и переотбора моделей нет. '
              'Парные95% customer-bootstrap интервалы разностей с H009/20,5000 повторов,seed42: paired_recall_differences.csv. '
              'Это диагностика уже просмотренных test-недель, не независимое подтверждение. '
              'Предыдущий novelty-аудит сохранён без изменений.', '', '![Recall](new_item_recall.png)']
    (REPORT / 'summary_ru.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    protocol()
    write(REPORT / 'verification.json', {'passed': True, 'six_full_catalog_replays': True, 'independent_AP': True,
          'original_references_unchanged': True, 'no_training': True, 'no_api': True, 'methods_on_plot': 17})
    write(REPORT / 'pipeline_status.json', {'status': 'pending_visual_review'})
    record('h010_h011_novelty_report', 'Six frozen-model exact top12 replays, independent AP and novelty recall complete; extended17-method graph generated, visual review pending.',
           RUN, status='pending_visual_review', artifacts=str(REPORT.relative_to(ROOT)))
    print(new[['method', 'mode', 'macro_recall', 'available_macro_recall']].to_string(index=False), flush=True)


def run():
    REPORT.mkdir(parents=True, exist_ok=True)
    with (REPORT / '.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        protocol()
        record('h010_h011_novelty_started', 'User requested H010/H011 recall under existing novelty protocol. Six frozen-model full-catalog scoring jobs, at most two concurrent CPU jobs; no fitting/API or model selection.',
               RUN, status='scoring', artifacts=str(REPORT.relative_to(ROOT)))
        def invoke(job):
            fold, key = job
            with (REPORT / f'{key}_fold{fold}.log').open('ab') as log:
                subprocess.run([sys.executable, '-u', str(Path(__file__).resolve()), 'score', '--fold', str(fold), '--method', key],
                               stdout=log, stderr=log, cwd=ROOT, check=True)
        try:
            jobs = [(fold, key) for fold in range(3) for key in LABELS]
            write(REPORT / 'pipeline_status.json', {'status': 'scoring', 'completed': 0, 'total': 6})
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(invoke, job) for job in jobs]
                for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
                    future.result()
                    write(REPORT / 'pipeline_status.json', {'status': 'scoring', 'completed': i, 'total': 6})
            report()
        except BaseException as error:
            write(REPORT / 'pipeline_status.json', {'status': 'interrupted', 'error': str(error)})
            record('h010_h011_novelty_interrupted', str(error), RUN, status='interrupted')
            raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['launch', 'run', 'score', 'report', 'review'])
    parser.add_argument('--fold', type=int, choices=range(3))
    parser.add_argument('--method', choices=list(LABELS))
    args = parser.parse_args()
    if args.action == 'launch':
        REPORT.mkdir(parents=True, exist_ok=True)
        with (REPORT / 'pipeline.log').open('ab') as log:
            child = subprocess.Popen([sys.executable, '-u', str(Path(__file__).resolve()), 'run'], cwd=ROOT,
                                     stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
        (REPORT / 'pipeline.pid').write_text(str(child.pid))
        print('Novelty controller PID', child.pid)
    elif args.action == 'run':
        run()
    elif args.action == 'score':
        score(args.fold, args.method)
    elif args.action == 'report':
        report()
    else:
        assert read(REPORT / 'verification.json')['passed']
        protocol()
        write(REPORT / 'pipeline_status.json', {'status': 'complete', 'visual_review_passed': True})
        record('h010_h011_novelty_complete', 'H010/H011 recall on ordinary and unseen-only recommendations verified; six exact full-catalog replays, independent AP, unchanged original references and17-method figure visually reviewed. No training/API.',
               RUN, status='complete', artifacts=str(REPORT.relative_to(ROOT)))
