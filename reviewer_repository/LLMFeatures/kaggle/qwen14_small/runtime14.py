"""Single-model reporting adapter; search/evaluator modules unchanged."""
from runtime import *

def finish(data, out, config_path):
    """Open final targets/references only after the14B feature selection are frozen."""
    data, out = Path(data), Path(out)
    config = json.loads(Path(config_path).read_text())
    smoke = config.get('validation_only_fake_callbacks', False)
    for name in ['qwen14b']:
        assert (out / name / 'selected.json').exists(), 'Select Qwen14B before test'
    rows, aps = [], {}
    programs = {'raw_control': out / 'raw_control'}
    for name in ['qwen14b']:
        selected = json.loads((out / name / 'selected.json').read_text())
        assert sha(Path(selected['directory']) / 'program.json') == selected['program_sha256']
        assert sha(Path(selected['directory']) / 'model.txt') == selected['model_sha256']
        programs[name + '_LightGBM'] = Path(selected['directory'])
    for name, directory in programs.items():
        row = {'model': name}
        for stage in ['heldout_val', 'val', 'test']:
            metric = evaluate(data, directory, stage, config_path)
            replay = evaluate(data, directory, 'replay_' + stage, config_path)
            assert replay['passed']
            row[stage + '_map_percent'] = 100 * metric['map']
            if stage == 'test':
                aps[name] = np.load(directory / 'test_ap.npy')
        rows.append(row)
    selection = json.loads((data / 'selection.json').read_text())
    sources = json.loads((data / 'references/sources.json').read_text())
    for source in sources:
        name = source['model']
        row = {'model': name}
        for split in ['val', 'test']:
            target = pd.read_parquet(data / f'{split}_targets.parquet')
            pred = np.load(data / f'references/{name}_{split}.npy')
            ap = ap12(pred, target.article_id)
            expected = source['metrics'][f'{split}_metrics']['map']
            assert abs(float(ap.mean()) - expected) < 1e-10, 'Reference alignment/metric mismatch: ' + name
            row[split + '_map_percent'] = 100 * float(ap.mean())
            if split == 'val':
                row['heldout_val_map_percent'] = 100 * float(ap[selection['heldout_val']].mean())
            else:
                aps[name] = ap
        rows.append(row)
    # Same time-safe popularity control used by the small ContextGNN report.
    tx = pd.read_parquet(data / 'transactions.parquet')
    row = {'model': 'popularity'}
    for split in ['val', 'test']:
        target = pd.read_parquet(data / f'{split}_targets.parquet')
        counts = tx[tx.t_dat <= target.timestamp.iloc[0]].article_id.value_counts().reindex(np.arange(5000), fill_value=0)
        ranking = np.lexsort((np.arange(5000), -counts.to_numpy()))[:12]
        ap = ap12(np.tile(ranking, (len(target), 1)), target.article_id)
        row[split + '_map_percent'] = 100 * float(ap.mean())
        if split == 'val':
            row['heldout_val_map_percent'] = 100 * float(ap[selection['heldout_val']].mean())
        else:
            aps['popularity'] = ap
    rows.append(row)
    frame = pd.DataFrame(rows)
    frame.to_csv(out / 'comparison.csv', index=False)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    for axis, split in zip(axes, ['val', 'test']):
        axis.barh(frame.model, frame[split + '_map_percent'])
        axis.set(title=split + ' — same small catalog5000', xlabel='MAP@12 (%)')
        axis.grid(axis='x', alpha=.2)
    if smoke:
        fig.suptitle('CPU SMOKE — fake Qwen14B responses; not LLM performance', color='darkred')
    fig.tight_layout()
    fig.savefig(out / 'comparison.png', dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for name in ['qwen14b_LightGBM', 'raw_control', 'contextgnn', 'lightgbm_manual']:
        values = aps[name]
        axes[0].hist(values[values > 0] * 100, bins=np.linspace(0, 100, 21), histtype='step', label=name)
        axes[1].bar(name, 100 * np.mean(values == 0))
    axes[0].set(xlabel='Per-user AP@12 (%) among AP>0', ylabel='Users', title='Test distribution')
    axes[0].legend(fontsize=7)
    axes[1].set(ylabel='Users with AP@12=0 (%)', ylim=(0, 100))
    axes[1].tick_params(axis='x', labelrotation=35)
    if smoke:
        fig.suptitle('CPU SMOKE — fake Qwen14B responses', color='darkred')
    fig.tight_layout()
    fig.savefig(out / 'test_histograms.png', dpi=160)
    plt.close(fig)
    fig, axis = plt.subplots(figsize=(8, 4))
    for name, directory in programs.items():
        curve = json.loads((directory / 'learning_curve.json').read_text())['train']['binary_logloss']
        axis.plot(np.arange(1, len(curve) + 1), curve, label=name)
    axis.set(xlabel='LightGBM round', ylabel='Training binary logloss', title='Loss is diagnostic; selection uses MAP@12')
    axis.legend()
    fig.tight_layout()
    fig.savefig(out / 'lightgbm_training.png', dpi=160)
    plt.close(fig)
    diff = aps['qwen14b_LightGBM'] - aps['raw_control']
    rng = np.random.default_rng(42)
    bootstrap = diff[rng.integers(0, len(diff), size=(10000, len(diff)))].mean(1) * 100
    write(out / 'paired_bootstrap.json', {'qwen14b_minus_raw_pp': float(diff.mean() * 100),
          'ci95_pp': np.quantile(bootstrap, [.025, .975]).tolist(), 'test_users': len(diff), 'seed': 42,
          'note': 'Exploratory paired-user interval, not multi-seed uncertainty'})
    lines = ['# Qwen14B — small H&M SQL feature search', '',
             'Same frozen small-v1 data,72813 train pairs,304val/250test users,all5000 catalog items.',
             'Qwen14B uses the original local-Qwen SQL JSON interface and NF4/FP16 loading.',
             'Old local Qwen used Q4_K_M/Ollama: this is not byte-identical quantization.',
             'Selection frozen before final test. Same20-success target/300-call cap/3repairs/3islands.',
             'Validation304 includes search/confirmation rows; heldout88 is separate for LLMs.',
             'References selected on original full validation, so their heldout88 is not an untouched selection set.',
             'Baselines have different model tuning/training/pretraining budgets. One seed;250test users.', '',
             '| Model | Val MAP,% | Test MAP,% |', '|---|---:|---:|']
    if smoke:
        lines.insert(1, '**CPU SMOKE ONLY: fake Qwen14B responses, not actual LLM performance.**')
    for record in rows:
        lines.append(f"| {record['model']} | {record['val_map_percent']:.5f} | {record['test_map_percent']:.5f} |")
    for name in ['qwen14b']:
        selected = json.loads((out / name / 'selected.json').read_text())
        lines += ['', f"{name}: {selected['successful_distinct']} successful /{selected['llm_calls']} calls; budget_complete={selected['budget_complete']}; selected_call={selected['call']} (null=raw control)."]
    lines += ['', '![Comparison](comparison.png)', '', '![Test AP histograms](test_histograms.png)']
    (out / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    budgets_complete = all(json.loads((out / name / 'selected.json').read_text())['budget_complete'] for name in ['qwen14b'])
    write(out / 'complete.json', {'status': 'complete' if budgets_complete else 'complete_with_incomplete_search',
                                'search_budgets_complete': budgets_complete, 'independent_frozen_replays': True,
                                'references_recomputed_from_predictions': True})
    archive_run(out)
    return frame
