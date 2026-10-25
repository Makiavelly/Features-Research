"""Audited H010 versus original H009-20, paired by customer and fold."""
import csv
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import ROOT, OLD, DATA, OUT, REPORT, RUN, read, write, sha


def audit(fold):
    folder = OUT / f'fold_{fold}'
    cfg = read(folder / 'run_config.json')
    sys.path.insert(0, str(folder / 'runtime'))
    from dialog_history import feedback
    trials = read(folder / cfg['arm'] / 'search_state.json')['trials']
    queries = []
    attempts = set()
    for trial in trials:
        generation = folder / 'generations' / f"call_{trial['call']:03d}"
        final = read(generation / 'final.json')
        assert final['island'] == trial['island']
        prefix = [{'role': 'system', 'content': cfg['system_message'] +
                   '\nThe query_train JSON research protocol below is also allowed. Before the first feature submission in each population, one train-statistics query is required; choose it yourself.'}]
        for prior in trials[:trial['call'] - 1]:
            if prior['island'] == trial['island']:
                prefix.extend(read(folder / 'generations' / f"call_{prior['call']:03d}" / 'final.json')['turns'])
        steps = sorted(generation.glob('step_*'))
        for index, step in enumerate(steps):
            response = read(step / 'response.json')
            attempt = response['api_attempt']
            assert attempt not in attempts
            attempts.add(attempt)
            request = read(folder / 'api_attempts' / f'attempt_{attempt:03d}' / 'request.json')
            assert request['messages'] == prefix + final['turns'][:1 + 2 * index]
            assert request['model'] == cfg['model_id']
            retry_path = step / 'explicit_retries.json'
            if retry_path.exists():
                for retry in read(retry_path):
                    failed = retry['failed_attempt']
                    assert failed not in attempts
                    attempts.add(failed)
                    failed_dir = folder / 'api_attempts' / f'attempt_{failed:03d}'
                    assert not (failed_dir / 'response.json').exists()
                    assert (failed_dir / 'failure.json').exists()
                    assert read(failed_dir / 'request.json')['messages'] == request['messages']
            if (step / 'tool_request.json').exists():
                command = read(step / 'tool_request.json')
                result = read(step / 'tool_result.json')
                assert command['island'] == trial['island']
                queries.append({'fold': fold, 'call': trial['call'], 'island': trial['island'],
                    'sql': command['command'].get('sql'), 'ok': result['ok'],
                    'result_rows': len(result.get('result', {}).get('rows', [])),
                    'error': result.get('error', '')})
    assert len(attempts) == len(list((folder / 'api_attempts').glob('attempt_*'))) <= 300
    assert sum(t['status'] == 'valid' for t in trials) == 20
    assert len(queries) <= 40
    for island, maximum in enumerate(cfg['research_island_budgets']):
        assert sum(q['island'] == island for q in queries) <= maximum
        assert any(q['island'] == island and q['ok'] for q in queries), 'Missing successful initial research'
    assert sha(folder / 'research.duckdb') == cfg['research_database_sha256']
    usage = []
    for path in sorted((folder / 'api_attempts').glob('attempt_*')):
        if (path / 'response.json').exists():
            result = read(path / 'response.json')
            u = result.get('usage', {})
            usage.append({'fold': fold, 'attempt': path.name, 'status': 'response',
                          'provider_model': result.get('model'),
                          'prompt_tokens': u.get('prompt_tokens'),
                          'completion_tokens': u.get('completion_tokens'),
                          'total_tokens': u.get('total_tokens')})
        else:
            failure = read(path / 'failure.json')
            usage.append({'fold': fold, 'attempt': path.name, 'status': 'failed',
                          'provider_model': None, 'prompt_tokens': None,
                          'completion_tokens': None, 'total_tokens': None,
                          'error': failure.get('error')})
    write(folder / 'research_audit.json', {'passed': True, 'exact_request_histories': True,
           'isolated_populations': True, 'queries': len(queries), 'actual_POST': len(attempts),
           'accepted_AST_programs': 20, 'database_hash_unchanged': True})
    return trials, queries, usage


def diversity(fold, trials):
    folder = OUT / f'fold_{fold}'
    resultpath = folder / 'sampled_matrix_diversity.json'
    if resultpath.exists():
        return read(resultpath)
    from python_features import FeatureEngine
    bundle = DATA / f'fold_{fold}/bundle'
    pairs = pd.read_parquet(bundle / 'train_pairs.parquet')
    cutoff = pairs.timestamp.max()
    sample = pairs[pairs.timestamp == cutoff].sample(n=64, random_state=42).reset_index(drop=True)
    engine = FeatureEngine(folder / 'scratch/diversity', bundle)
    results = []
    try:
        for trial in trials:
            if trial['status'] != 'valid':
                continue
            path = Path(trial['directory'])
            program = read(path / 'program.json')
            engine.prepare(cutoff, sample.customer_id.to_numpy(), program)
            frame = engine.frame(sample)
            values = np.nan_to_num(frame.to_numpy(dtype=np.float32), nan=-1., posinf=-1., neginf=-1.)
            columns = sorted(hashlib.sha256(values[:, i].copy().tobytes()).hexdigest() for i in range(values.shape[1]))
            signature = hashlib.sha256(json.dumps(columns).encode()).hexdigest()
            results.append({'call': trial['call'], 'features': values.shape[1], 'sample_matrix_sha256': signature})
    finally:
        engine.close()
    result = {'programs': results, 'sample_rows': 64, 'cutoff': str(cutoff),
              'distinct_sample_matrices': len(set(x['sample_matrix_sha256'] for x in results)),
              'note': 'Equality on a64-row train sample is a diagnostic, not proof of full-matrix equality; column names/order ignored.'}
    write(resultpath, result)
    return result


def main():
    folds, queries, usage, candidates, diversity_rows = [], [], [], [], []
    method_ap = {'h010': [], 'h009_20': []}
    users = []
    for fold in range(3):
        folder = OUT / f'fold_{fold}'
        assert read(folder / 'verification.json')['passed']
        trials, q, u = audit(fold)
        queries += q
        usage += u
        div = diversity(fold, trials)
        diversity_rows.append({'fold': fold, **div})
        cfg = read(folder / 'run_config.json')
        selected = read(folder / cfg['arm'] / 'selected.json')
        h010_ap = np.load(folder / 'test_ap.npy')
        baseline = OLD / f'fold_{fold}/h009'
        h009_ap = np.load(baseline / 'test_ap.npy')
        baseline_users = np.load(baseline / 'test_users.npy')
        current_users = np.load(folder / 'test_users.npy')
        np.testing.assert_array_equal(current_users, baseline_users)
        assert h010_ap.shape == h009_ap.shape
        method_ap['h010'].append(h010_ap)
        method_ap['h009_20'].append(h009_ap)
        users.append(current_users)
        folds.append({'fold': fold, 'users': len(h010_ap), 'h010_test_map': float(h010_ap.mean()),
                      'h009_20_test_map': float(h009_ap.mean()),
                      'difference_pp': float((h010_ap - h009_ap).mean() * 100),
                      'selected_call': selected['call'], 'confirmation_map': selected['confirmation_map'],
                      'queries': len(q), 'actual_POST': len(u),
                      'distinct_sample_matrices': div['distinct_sample_matrices']})
        for trial in trials:
            candidates.append({'fold': fold, 'call': trial['call'], 'island': trial['island'],
                               'status': trial['status'], 'search_map': trial.get('score'),
                               'failure_stage': trial.get('failure_stage'),
                               'research_queries': trial.get('research_queries_this_generation', 0)})
        selected_dir = Path(selected['directory'])
        target = REPORT / f'selected_programs/fold_{fold}.py'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text((selected_dir / 'program.py').read_text(encoding='utf-8'), encoding='utf-8')
    users = np.concatenate(users)
    methods = {k: np.concatenate(v) for k, v in method_ap.items()}
    unique, inverse = np.unique(users, return_inverse=True)
    counts = np.bincount(inverse)
    sums = {k: np.bincount(inverse, weights=v) for k, v in methods.items()}
    rng = np.random.default_rng(42)
    boot = {k: [] for k in methods}
    for _ in range(5000):
        sample = rng.integers(0, len(unique), len(unique))
        denominator = counts[sample].sum()
        for key in boot:
            boot[key].append(sums[key][sample].sum() / denominator)
    result = {'protocol': RUN, 'folds': folds, 'users_times': len(users), 'unique_customers': len(unique),
              'bootstrap_replicates': 5000, 'bootstrap_unit': 'customer retaining all fold observations',
              'methods': {k: {'pooled_map': float(v.mean()),
                               'equal_fold_mean_map': float(np.mean([x.mean() for x in method_ap[k]])),
                               'ci95': np.quantile(boot[k], [.025, .975]).tolist()}
                          for k, v in methods.items()},
              'difference_pp': float((methods['h010'] - methods['h009_20']).mean() * 100),
              'difference_ci95_pp': (np.quantile(np.asarray(boot['h010']) - np.asarray(boot['h009_20']), [.025, .975]) * 100).tolist(),
              'test_previously_inspected': True, 'new_outer_labels_used_for_selection': False,
              'research_queries': len(queries), 'actual_POST': len(usage),
              'prompt_tokens': sum(x['prompt_tokens'] or 0 for x in usage),
              'completion_tokens': sum(x['completion_tokens'] or 0 for x in usage),
              'attempts_with_unknown_token_usage': sum(x['prompt_tokens'] is None or x['completion_tokens'] is None for x in usage)}
    write(REPORT / 'comparison.json', result)
    write(REPORT / 'sampled_matrix_diversity.json', diversity_rows)
    for name, rows in [('fold_metrics', folds), ('research_queries', queries), ('api_usage', usage), ('candidate_metrics', candidates)]:
        pd.DataFrame(rows).to_csv(REPORT / f'{name}.csv', index=False)
    pd.DataFrame({'customer_id': users, 'h010_AP': methods['h010'], 'h009_20_AP': methods['h009_20'],
                  'difference': methods['h010'] - methods['h009_20']}).to_csv(REPORT / 'paired_AP.csv', index=False)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    labels = ['H009 /20', 'H010 research /20']
    keys = ['h009_20', 'h010']
    means = np.array([result['methods'][k]['pooled_map'] for k in keys]) * 100
    ci = np.array([result['methods'][k]['ci95'] for k in keys]) * 100
    axes[0].bar(labels, means, color=['#6b7280', '#2563eb'])
    axes[0].errorbar(range(2), means, yerr=np.array([means - ci[:, 0], ci[:, 1] - means]), fmt='none', color='black', capsize=4)
    axes[0].set(ylabel='Pooled test MAP@12 (%)', title='Same20 accepted programs per fold')
    x = np.arange(3)
    axes[1].bar(x - .18, [f['h009_20_test_map'] * 100 for f in folds], .36, label=labels[0], color='#6b7280')
    axes[1].bar(x + .18, [f['h010_test_map'] * 100 for f in folds], .36, label=labels[1], color='#2563eb')
    axes[1].set(xticks=x, xticklabels=['fold0', 'fold1', 'fold2'], ylabel='Test MAP@12 (%)', title='Temporal folds')
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(REPORT / 'comparison.png', dpi=160)
    fig.savefig(REPORT / 'comparison.svg')
    plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    for fold in range(3):
        folder = OUT / f'fold_{fold}'
        cfg = read(folder / 'run_config.json')
        trials = read(folder / cfg['arm'] / 'search_state.json')['trials']
        accepted = [t for t in trials if t['status'] == 'valid']
        axes[fold].scatter(range(1, 21), [t['score'] * 100 for t in accepted], c=[t['island'] for t in accepted], cmap='viridis', vmin=0, vmax=2, label='H010 candidates')
        axes[fold].plot(range(1, 21), np.maximum.accumulate([t['score'] * 100 for t in accepted]), color='#2563eb', label='H010 best search')
        oldcfg = read(OLD / f'fold_{fold}/h009/run_config.json')
        oldtrials = read(OLD / f"fold_{fold}/h009/{oldcfg['arm']}/search_state.json")['trials']
        scores = [t['score'] * 100 for t in oldtrials if t['status'] == 'valid']
        axes[fold].plot(range(1, len(scores) + 1), np.maximum.accumulate(scores), '--', color='#6b7280', label='H009 best search')
        axes[fold].set(title=f'Fold{fold}', xlabel='Accepted programs', ylabel='Search MAP@12 (%)')
        axes[fold].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(REPORT / 'search_curves.png', dpi=160)
    plt.close(fig)
    low, high = result['difference_ci95_pp']
    lines = ['# H010: исследование train-данных через API', '',
        'Сопоставление с исходным H009 при20 проверенных программах на каждый фолд. Три временных фолда, seed42, одинаковые train-пары, каталог10000 и LightGBM. Единственное запланированное изменение — SQL-инструмент исследования train-данных и сохранение его ответов в собственной истории популяции.', '',
        '| Метод | Pooled test MAP@12 | 95% customer-bootstrap |', '|---|---:|---:|']
    for key, label in zip(keys, labels):
        m = result['methods'][key]
        lines.append(f"|{label}|{m['pooled_map'] * 100:.4f}%|[{m['ci95'][0] * 100:.4f}%; {m['ci95'][1] * 100:.4f}%]|")
    lines += ['', f"Разница H010−H009: {result['difference_pp']:+.4f}п.п.; парный95% интервал [{low:+.4f}; {high:+.4f}]п.п.", '',
        '| Фолд | H009 | H010 | Разница, п.п. | Запросы статистики | API POST |', '|---|---:|---:|---:|---:|---:|']
    for f in folds:
        lines.append(f"|{f['fold']}|{f['h009_20_test_map'] * 100:.4f}%|{f['h010_test_map'] * 100:.4f}%|{f['difference_pp']:+.4f}|{f['queries']}|{f['actual_POST']}|")
    lines += ['', f"Всего{len(queries)} исследовательских запросов;{len(usage)} API POST; известные input/output токены:{result['prompt_tokens']}/{result['completion_tokens']}.",
        'Все60 AST-программ проверены. Сохранены выбранные программы, полные запросы/ответы, SQL и результаты. Победители зафиксированы до новой outer-оценки; полные frozen replays и независимый AP прошли. Аудит проверил точную историю каждого фактического API-запроса, изоляцию популяций и лимиты.', '',
        'Bootstrap:5000 повторов по исходным покупателям с сохранением их наблюдений во всех фолдах, seed42. Это неопределённость для данных недель и фиксированных моделей. Один поиск/seed; бюджеты программ равны, расходы токенов, объём информации и исследовательских вычислений различаются. Нельзя приписывать всю стохастическую разницу только инструментам.',
        'Test-недели ранее просматривались. Это внутренний эксперимент; подтверждение на новых неделях требует отдельного протокола. Неиспользуемые каталожные цели сохранены в знаменателе MAP. Старые результаты не изменены.', '',
        'Предварительная optional-tool серия v1 остановлена без outer-оценки после первых ответов без исследовательских запросов. Её программы не переиспользованы и не входят в60 программ v2; её API-затраты сохранены отдельно в reports/medium_h010_research_v1/. Правило обязательного первого исследования зафиксировано до запросов v2.', '',
        'Диагностика численных дубликатов: sampled_matrix_diversity.json,64 фиксированные train-пары последнего cutoff каждого фолда; совпадение на выборке не доказывает совпадения полных матриц. AST-уникальность сама по себе не означает уникальность значений.', '',
        '![Сравнение](comparison.png)', '', '![Поиск](search_curves.png)', '',
        'Артефакты: comparison.json, fold_metrics.csv, research_queries.csv, api_usage.csv, candidate_metrics.csv, paired_AP.csv, selected_programs/.']
    (REPORT / 'summary_ru.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    write(REPORT / 'complete.json', {'status': 'pending_visual_review', 'all60_accepted': True,
          'full_replays': True, 'exact_dialog_audits': True})
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
