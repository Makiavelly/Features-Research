"""Generation efficiency is separate from recommendation quality."""
def efficiency_report(out, config):
    rows = []
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for arm in config['arms']:
        trials = json.loads((out / arm / 'search_state.json').read_text())['trials']
        row = {'arm': arm, 'calls': len(trials)}
        row.update({s: sum(t['status'] == s for t in trials) for s in ['valid', 'rejected', 'duplicate']})
        row.update(repair_calls=sum(t['repair'] > 0 for t in trials),
                   unchanged_repairs=sum(t.get('unchanged_repair', False) for t in trials),
                   generated_tokens=sum(t.get('generated_tokens', 0) for t in trials),
                   generation_seconds=sum(t.get('seconds', 0) for t in trials),
                   evaluation_and_generation_seconds=sum(t.get('elapsed_seconds', 0) for t in trials),
                   target_reached=row['valid'] == config['target_successful_distinct'])
        rows.append(row)
        valid = [t for t in trials if t['status'] == 'valid']
        axes[0].step([0] + [t['call'] for t in valid], [0] + list(range(1, len(valid) + 1)), where='post', label=arm)
    frame = pd.DataFrame(rows)
    frame.to_csv(out / 'generation_efficiency.csv', index=False)
    axes[0].set(xlabel='LLM calls', ylabel='Distinct measured sets', title='Calls to measured sets')
    axes[0].legend()
    frame.set_index('arm')[['valid', 'rejected', 'duplicate']].plot.bar(stacked=True, ax=axes[1])
    axes[1].set(title='All calls counted', ylabel='Calls')
    axes[2].bar(frame.arm, frame.generation_seconds / 60)
    axes[2].set(title='Generation time', ylabel='Minutes')
    if config.get('validation_only_fake_callbacks'):
        fig.suptitle('CPU SMOKE: scripted responses, not LLM performance', color='darkred')
    fig.tight_layout()
    fig.savefig(out / 'generation_efficiency.png', dpi=160)
    plt.close(fig)
    with (out / 'report.md').open('a', encoding='utf-8') as stream:
        stream.write('\n\nH003 arms: A=diagnostics; B=A+prompt examples; C=B+duplicate/unchanged policy.\n'
                     'Compare each adjacent variant, and A to the previous archived Qwen7B control.\n'
                     'The same previously inspected test is reused diagnostically, never to select variants.\n'
                     'See generation_efficiency.csv and generation_efficiency.png.\n')
