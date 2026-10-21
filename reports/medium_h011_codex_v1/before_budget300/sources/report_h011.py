"""Parent-only final H011 comparison; never called during agent search."""
import json
from pathlib import Path
import shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from h011_stage import ROOT, OUT, REPORT, OLD, RUN, read, write, record, sha


def response_usage(path):
    raw = Path(path).read_text(encoding='utf-8', errors='replace')
    try:
        result = json.loads(raw)
        return result.get('usage'), result.get('model')
    except ValueError:
        pass
    for line in raw.splitlines():
        if line.startswith('data:'):
            try:
                event = json.loads(line[5:].strip())
            except ValueError:
                continue
            if event.get('type') == 'response.completed':
                result = event['response']
                return result.get('usage'), result.get('model')
    return None, None


def main():
    resultrows, uses, hypotheses = [], [], []
    users, current, baseline = [], [], []
    frozen = read(REPORT / 'pretest_freeze.json')
    for fold in range(3):
        folder = OUT / f'fold_{fold}'
        assert read(folder / 'verification.json')['passed']
        state = read(folder / 'budget.json')
        assert len(state['accepted']) == 20
        selected = read(folder / 'selected.json')
        winner = Path(selected['directory'])
        assert sha(winner / 'program.json') == frozen['folds'][str(fold)]['program_sha256']
        assert sha(winner / 'model.txt') == frozen['folds'][str(fold)]['model_sha256']
        own = np.load(folder / 'test_ap.npy')
        other = np.load(OLD / f'fold_{fold}/h009/test_ap.npy')
        ids = np.load(folder / 'test_users.npy')
        np.testing.assert_array_equal(ids, np.load(OLD / f'fold_{fold}/h009/test_users.npy'))
        users.append(ids)
        current.append(own)
        baseline.append(other)
        research = read(folder / 'research_budget.json')
        assert all(n <= cap for n, cap in zip(research, [14, 13, 13]))
        attempts = sorted((folder / 'api_attempts').glob('attempt_*'))
        assert len(attempts) <= 300
        for path in attempts:
            request = read(path / 'request.json')
            origin = read(path / 'origin.json')
            assert origin['fold'] == fold and origin['island'] in range(3)
            assert request['model'] == 'gpt-6.1-sol'
            assert request['reasoning']['effort'] == 'low' and request['temperature'] == .8
            assert request['max_output_tokens'] == 2048
            usage, model = response_usage(path / 'response.raw') if (path / 'response.raw').exists() else (None, None)
            uses.append({'fold': fold, 'island': origin['island'], 'attempt': path.name,
                         'provider_model': model, 'input_tokens': usage.get('input_tokens') if usage else None,
                         'output_tokens': usage.get('output_tokens') if usage else None,
                         'failed': (path / 'failure.json').exists()})
        resultrows.append({'fold': fold, 'users': len(ids), 'h011_map': float(own.mean()),
                           'h009_20_map': float(other.mean()), 'difference_pp': float((own - other).mean() * 100),
                           'selected_call': selected['call'], 'confirmation_map': selected['confirmation_map'],
                           'research_requests': sum(research), 'actual_POST': len(attempts)})
        hypotheses.extend({'fold': fold, **{k: v for k, v in a.items() if k != 'directory'}} for a in state['attempts'])
        target = REPORT / f'selected_programs/fold_{fold}.py'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text((winner / 'program.py').read_text(encoding='utf-8'), encoding='utf-8')
    users, current, baseline = map(np.concatenate, [users, current, baseline])
    unique, inv = np.unique(users, return_inverse=True)
    n = np.bincount(inv)
    sums = np.array([np.bincount(inv, weights=a) for a in [current, baseline]])
    rng = np.random.default_rng(42)
    samples = []
    for _ in range(5000):
        ids = rng.integers(0, len(unique), len(unique))
        samples.append(sums[:, ids].sum(axis=1) / n[ids].sum())
    samples = np.asarray(samples)
    intervals = np.quantile(samples, [.025, .975], axis=0)
    delta_ci = np.quantile(samples[:, 0] - samples[:, 1], [.025, .975]) * 100
    result = {'protocol': RUN, 'users_times': len(users), 'unique_customers': len(unique),
              'h011_pooled_map': float(current.mean()), 'h009_20_pooled_map': float(baseline.mean()),
              'ci95_h011': intervals[:, 0].tolist(), 'ci95_h009_20': intervals[:, 1].tolist(),
              'difference_pp': float((current - baseline).mean() * 100),
              'difference_ci95_pp': delta_ci.tolist(), 'folds': resultrows,
              'bootstrap_replicates': 5000, 'bootstrap_unit': 'customer retaining all folds',
              'known_input_tokens': sum(u['input_tokens'] or 0 for u in uses),
              'known_output_tokens': sum(u['output_tokens'] or 0 for u in uses),
              'unknown_usage_attempts': sum(u['input_tokens'] is None for u in uses),
              'test_previously_inspected': True}
    write(REPORT / 'comparison.json', result)
    for name, rows in [('fold_metrics', resultrows), ('api_usage', uses), ('hypotheses_and_trials', hypotheses)]:
        pd.DataFrame(rows).to_csv(REPORT / f'{name}.csv', index=False)
    pd.DataFrame({'customer_id': users, 'h011_AP': current, 'h009_20_AP': baseline,
                  'difference': current - baseline}).to_csv(REPORT / 'paired_AP.csv', index=False)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    means = np.array([baseline.mean(), current.mean()]) * 100
    cis = intervals[:, [1, 0]] * 100
    axes[0].bar(['H009 /20', 'Codex H011 /20'], means, color=['#6b7280', '#7c3aed'])
    axes[0].errorbar([0, 1], means, yerr=np.maximum(0, [means - cis[0], cis[1] - means]), fmt='none', color='black', capsize=4)
    axes[0].set(ylabel='Pooled test MAP@12 (%)', title='20 accepted programs per fold')
    x = np.arange(3)
    axes[1].bar(x - .18, [r['h009_20_map'] * 100 for r in resultrows], .36, label='H009', color='#6b7280')
    axes[1].bar(x + .18, [r['h011_map'] * 100 for r in resultrows], .36, label='H011 Codex', color='#7c3aed')
    axes[1].set(xticks=x, xticklabels=['fold0', 'fold1', 'fold2'], ylabel='Test MAP@12 (%)')
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(REPORT / 'comparison.png', dpi=160)
    fig.savefig(REPORT / 'comparison.svg')
    plt.close(fig)
    lines = ['# H011: автономный Codex GPT-6.1 Sol', '',
             'Три отдельные популяции на каждом из трёх исходных medium-v2 фолдов. Агент сам исследовал train-данные в изолированном терминале, записывал гипотезы и проверял программы через прежний оценщик H009. Все60 проверок завершены; выборы зафиксированы до новой outer-оценки, полные replay и независимый AP прошли.', '',
             '| Метод | Pooled test MAP@12 | 95% customer-bootstrap |', '|---|---:|---:|',
             f'|H009 /20|{baseline.mean() * 100:.4f}%|[{intervals[0, 1] * 100:.4f}%; {intervals[1, 1] * 100:.4f}%]|',
             f'|H011 Codex /20|{current.mean() * 100:.4f}%|[{intervals[0, 0] * 100:.4f}%; {intervals[1, 0] * 100:.4f}%]|', '',
             f"Разница H011−H009: {result['difference_pp']:+.4f}п.п.; парный95% интервал [{delta_ci[0]:+.4f}; {delta_ci[1]:+.4f}]п.п.", '',
             'Bootstrap:5000 выборок исходных покупателей с сохранением их наблюдений по фолдам, seed42. Фолды и расходы — fold_metrics.csv и api_usage.csv. Гипотезы/ошибки — hypotheses_and_trials.csv; код — selected_programs/.', '',
             'Это отдельный агентный протокол: системные инструкции Codex, native tools, контекст, расходы и управление sampling отличаются от H009/H010. Равны бюджеты20 успешных программ, но не токены или вычисления. Один seed; test-недели уже просматривались. Новых временных режимов и независимых повторных обучений этот опыт не подтверждает. Исходные цели вне каталога сохранены в знаменателе MAP. AST-уникальность не доказывает численную уникальность признаков.', '',
             '![Сравнение](comparison.png)', '',
             'График требует визуальной проверки перед окончательным закрытием эксперимента.']
    (REPORT / 'summary_ru.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    write(REPORT / 'complete.json', {'status': 'report_pending_visual_review', 'all60_accepted': True, 'full_replays': True})
    record('h011_report_generated', 'All60 native Codex programs, three frozen selections, full replays and independent AP complete; comparison generated, visual review pending.',
           RUN, status='report_pending_visual_review', artifacts=str(REPORT.relative_to(ROOT)))


if __name__ == '__main__':
    main()
