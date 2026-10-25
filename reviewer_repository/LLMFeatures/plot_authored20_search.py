"""Plot saved search results only; never fits models or reads final targets."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9'
OUT = ROOT / 'reports/authored20_v1/plots'
OUT.mkdir(parents=True, exist_ok=True)
trials = json.loads((RUN / 'state.json').read_text(encoding='utf-8'))['trials']
assert len(trials) == 20 and all(t['status'] == 'valid' for t in trials)
numbers = np.array([t['call'] for t in trials])
scores = np.array([t['score'] * 100 for t in trials])
islands = np.array([t['island'] for t in trials])
assert np.array_equal(numbers, np.arange(1, 21))
best = trials[int(np.argmax(scores))]
def candidate(t):
    return RUN / 'codex_authored20/candidates' / f"candidate_{t['call']:03d}"
raw = RUN / 'raw_control'
control = json.loads((raw / 'search_metrics.json').read_text())['map'] * 100
colors = ['#2166ac', '#d95f02', '#1b9e77']
for t in trials:
    ap = np.load(candidate(t) / 'search_ap.npy')
    assert len(ap) == 128
    np.testing.assert_allclose(ap.mean(), t['score'], rtol=0, atol=1e-14)

def progress(ax):
    ax.plot(numbers, scores, color='0.8', lw=1, zorder=0)
    for i, c in enumerate(colors):
        mask = islands == i
        ax.scatter(numbers[mask], scores[mask], color=c, label=f'Population {i}', zorder=3)
    ax.axhline(control, color='0.35', ls='--', label='Raw15 control')
    ax.set(xlabel='Evaluated set', ylabel='Search MAP@12 (%)', title='Adaptive search: all 20 sets', xticks=np.arange(1, 21, 2))
    ax.legend(fontsize=8)

def population(ax):
    for i, c in enumerate(colors):
        mask = islands == i
        ax.step(numbers[mask], np.maximum.accumulate(np.maximum(scores[mask], control)), where='post', color=c, marker='o', label=f'Population {i}')
    ax.axhline(control, color='0.35', ls='--', label='Raw15 control')
    ax.set(xlabel='Evaluated set', ylabel='Best search MAP@12 (%)', title='Best-so-far within each population')
    ax.legend(fontsize=8)

def bars(ax):
    ax.bar(numbers, scores, color=[colors[i] for i in islands])
    ax.axhline(control, color='0.35', ls='--', label='Raw15 control')
    ax.set(xlabel='Set number', ylabel='Search MAP@12 (%)', title='Search scores by feature set', xticks=np.arange(1, 21, 2))
    ax.legend(fontsize=8)

def histogram(ax):
    ax.hist(scores, bins=np.linspace(0, max(scores)*1.06, 9), color='#4575b4', edgecolor='white')
    ax.axvline(control, color='0.35', ls='--', label='Raw15 control')
    ax.set(xlabel='Search MAP@12 (%)', ylabel='Number of sets', title='Distribution across 20 evaluated sets')
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.legend(fontsize=8)

def user_hist(ax):
    bins = np.linspace(0, 1, 21)
    for path, label, color in [(raw, 'Raw15 control', '0.45'), (candidate(best), f"Search leader: set {best['call']}", colors[best['island']])]:
        ap = np.load(path / 'search_ap.npy')
        ax.hist(ap, bins=bins, histtype='step', lw=2, color=color, label=f'{label} ({np.count_nonzero(ap == 0)}/128 zero)')
    ax.set(xlabel='Per-user AP@12 (fraction)', ylabel='Users', title='Search users: AP@12 distribution')
    ax.legend(fontsize=8)

def loss(ax):
    for t in trials:
        curve = json.loads((candidate(t) / 'learning_curve.json').read_text())['train']['binary_logloss']
        ax.plot(np.arange(1, len(curve)+1), curve, color=colors[t['island']], alpha=.4, lw=1)
    ax.set(xlabel='Boosting round', ylabel='Training binary logloss', title='Training curves: all 20 LightGBM models')

functions = [('search_progress', progress), ('population_best', population), ('all20_scores', bars), ('scores_histogram', histogram), ('users_ap_histogram', user_hist), ('training_curves', loss)]
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
for name, draw in functions:
    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
    draw(ax)
    ax.grid(axis='y', alpha=.18)
    fig.savefig(OUT / f'{name}.png', dpi=160)
    fig.savefig(OUT / f'{name}.svg')
    plt.close(fig)
fig, axes = plt.subplots(3, 2, figsize=(15, 14), constrained_layout=True)
for ax, (_, draw) in zip(axes.flat, functions):
    draw(ax)
    ax.grid(axis='y', alpha=.18)
fig.suptitle('Authored20: SEARCH results only | generated features + raw15\nNot a blind experiment; final validation/test comparison is shown separately', fontsize=14)
fig.savefig(OUT / 'search_dashboard.png', dpi=150)
plt.close(fig)
print(f'Created dashboard + 6 plots (PNG/SVG): {OUT}')
print('Verified all 20 saved per-user AP means match search scores.')
