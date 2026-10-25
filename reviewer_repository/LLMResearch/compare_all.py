"""Plot verified existing test results together; no fitting or model selection."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/medium_all_methods_h011_v1'
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / 'RelBenchGNN'))
from tracking import record


def read(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8'))


original = 'reports/medium_followup_v1/final_comparison/comparison.json'
h010path = 'reports/medium_h010_research_v2/comparison.json'
h011path = 'reports/medium_h011_codex_budget300_v2/comparison.json'
old, h010, h011 = map(read, [original, h010path, h011path])
assert old['status'] == 'passed'
for directory in ['medium_h010_research_v2', 'medium_h011_codex_budget300_v2']:
    assert read(f'reports/{directory}/complete.json')['status'] == 'complete'
rows = old['summary'].copy()
rows.append({'method': 'h010_20', 'label': 'H010: SQL-исследования / 20',
             'pooled_map': h010['methods']['h010']['pooled_map'],
             'ci95_low': h010['methods']['h010']['ci95'][0],
             'ci95_high': h010['methods']['h010']['ci95'][1],
             'fold_maps': [r['h010_test_map'] for r in h010['folds']]})
rows.append({'method': 'h011_20', 'label': 'H011: автономный Codex / 20',
             'pooled_map': h011['h011_pooled_map'],
             'ci95_low': h011['ci95_h011'][0], 'ci95_high': h011['ci95_h011'][1],
             'fold_maps': [r['h011_map'] for r in h011['folds']]})
weights = np.array([1839, 1982, 1698])
for row in rows:
    assert abs(np.average(row['fold_maps'], weights=weights) - row['pooled_map']) < 1e-12
    assert row['ci95_low'] <= row['pooled_map'] <= row['ci95_high']
assert len({r['method'] for r in rows}) == len(rows) == 16
rows.sort(key=lambda r: -r['pooled_map'])
colors = {'h010_20': '#1976d2', 'h011_20': '#7c3aed', 'h009_20': '#ea8c24'}


def draw(selected, filename, title, xmax, height):
    fig, ax = plt.subplots(figsize=(13, height), facecolor='white')
    fig.subplots_adjust(left=.33, right=.97, top=.82 if height < 7 else .89, bottom=.16 if height < 7 else .13)
    positions = np.arange(len(selected))
    values = np.array([r['pooled_map'] * 100 for r in selected])
    low = np.array([r['ci95_low'] * 100 for r in selected])
    high = np.array([r['ci95_high'] * 100 for r in selected])
    ax.barh(positions, values, height=.65,
            color=[colors.get(r['method'], '#9aa7b6') for r in selected], zorder=2)
    ax.errorbar(values, positions, xerr=[values - low, high - values],
                fmt='none', ecolor='#354254', capsize=3, linewidth=1.1, zorder=3)
    for y, r in zip(positions, selected):
        label = f"{r['pooled_map'] * 100:.4f}%".replace('.', ',')
        ax.text(xmax * .985, y, label, ha='right', va='center', fontsize=10,
                fontweight='bold' if r['method'] in colors else 'normal')
    ax.set(yticks=positions, yticklabels=[r['label'] for r in selected],
           xlim=(0, xmax), xlabel='Test MAP@12, % — среднее по всем 5519 наблюдениям')
    ax.invert_yaxis()
    ax.xaxis.grid(True, alpha=.18, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis='y', length=0, pad=10)
    for side in ['top', 'right', 'left']:
        ax.spines[side].set_visible(False)
    fig.suptitle(title, fontsize=17, fontweight='bold', x=.04, ha='left', y=.975)
    fig.text(.04, .89 if height < 7 else .93,
             '3 временных фолда · 20 000 покупателей · каталог 10 000 товаров · seed 42', fontsize=10, color='#526071')
    fig.text(.04, .055 if height < 7 else .055,
             'Усы: 95% bootstrap по покупателям, 5000 повторов. Один seed; test-недели ранее просматривались.',
             fontsize=9, color='#526071')
    fig.text(.04, .02,
             'H011: лимит исследований повышен 40 → 300 во время поиска; равное число программ не означает равные расходы.',
             fontsize=9, color='#526071')
    fig.savefig(OUT / f'{filename}.png', dpi=180)
    fig.savefig(OUT / f'{filename}.svg')
    plt.close(fig)


draw(rows, 'comparison_all', 'H011 в сравнении с остальными методами', 1.72, 10)
matched = [r for r in rows if r['method'] in ['h008_20', 'h009_20', 'h010_20', 'h011_20', 'manual']]
assert len(matched) == 5
draw(matched, 'comparison_budget20', 'LLM-поиск: по 20 принятых программ на фолд', .79, 5.8)
pd.DataFrame([{**r, 'fold_maps': json.dumps(r['fold_maps'])} for r in rows]).to_csv(OUT / 'summary.csv', index=False)
manifest = {'methods': rows, 'weights': weights.tolist(), 'users_times': 5519,
            'metric': 'full-target pooled test MAP@12', 'bootstrap': 'customer,5000 replicates,seed42',
            'sources_sha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                               for p in [original, h010path, h011path]},
            'status': 'pending_visual_review', 'new_training': False}
(OUT / 'comparison.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
lines = ['# Сравнение методов с H010 и H011', '',
         'Одинаковые три medium-v2 фолда, каталог и исходные test-цели. Pooled MAP взвешен по1839/1982/1698 наблюдениям.', '',
         '![Все методы](comparison_all.png)', '', '![Бюджет20](comparison_budget20.png)', '',
         '| Метод | Test MAP@12 | Фолд0 | Фолд1 | Фолд2 |', '|---|---:|---:|---:|---:|']
for r in rows:
    lines.append('|' + r['label'] + '|' + '|'.join(f'{v*100:.4f}%' for v in [r['pooled_map'], *r['fold_maps']]) + '|')
lines += ['', 'Усы: ранее рассчитанные95% customer-bootstrap интервалы,5000 повторов,seed42; '
          'это неопределённость для фиксированных моделей и недель, не разброс повторных обучений. '
          'Один seed, test-недели уже просматривались. Бюджеты20/30/40 — продолжения поисков, не независимые повторы. '
          'H011 продолжен после увеличения исследовательского бюджета40→300 на первом фолде. '
          'Равенство числа программ не означает равенство токенов, вычислений или инструкций. '
          'Новые ContextGNN validation-only опыты не включены в test-сравнение. '
          'Ограничение численного replay ContextGNN fold2 описано в исходном final_comparison/report.md.', '',
          'Источники и ихSHA256: comparison.json. Таблица: summary.csv. Новых обучений и API-запросов не было.']
(OUT / 'summary_ru.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
record('h011_all_methods_plot_generated', 'Combined16 verified existing methods, including H010/H011, on identical three-fold pooled test metric; budget20 detail also generated. No fitting/API; visual review pending.',
       'hm_medium_all_methods_h011_plot_v1', status='pending_visual_review', artifacts=str(OUT.relative_to(ROOT)))
print(OUT)
