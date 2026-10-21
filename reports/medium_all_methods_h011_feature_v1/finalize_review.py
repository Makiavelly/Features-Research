"""Run after inspecting comparison_all.png visually; keep original artifacts intact."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'CVFollowup'))
from common import read, write, sha, record

REP = Path(__file__).resolve().parent
DEST = ROOT / 'CVFollowup/results/v1/feature_test_comparison_v1'
frozen = read(REP / 'pretest_freeze.json')
for name, digest in {**frozen['reference_hashes'], **frozen['sources']}.items():
    assert sha(ROOT / name) == digest, name
summary = read(REP / 'comparison.json')
original = read(ROOT / 'reports/medium_all_methods_h011_v1/comparison.json')
assert len(summary['methods']) == 17
for row in original['methods']:
    assert next(r for r in summary['methods'] if r['method'] == row['method']) == row
checks = [read(DEST / f'fold_{f}/feature/verification.json') for f in range(3)]
assert all(c['passed_scores'] for c in checks)
assert [c['rows'] for c in checks] == [1839, 1982, 1698]
assert summary['users_times'] == 5519 and summary['customers'] == 4548
assert all((REP / f'comparison_all.{extension}').stat().st_size > 10000 for extension in ['png', 'svg'])
changed = sum(len(c['top12_changed_rows']) for c in checks)
sensitivity = max(c['max_per_user_ap_difference'] for c in checks)
review = dict(passed=True, image='comparison_all.png', methods=17,
    checks=['All 17 labels and values fit', 'FEATURE highlighted in green',
            'Confidence intervals visible', 'Title, axis and footnotes readable'])
write(REP / 'visual_review.json', review)
status = 'complete_verified_plot' if not changed else 'complete_plot_with_replay_qualification'
summary.update(status=status, replay_changed_rows=changed, max_per_user_ap_replay_sensitivity=sensitivity)
write(REP / 'comparison.json', summary)
write(REP / 'final_verification.json', dict(status=status,
    references_and_sources_unchanged=True, original_16_rows_unchanged=True,
    checkpoint_files_unchanged=True, test_rows=5519, customers=4548,
    no_training=True, no_reselection=True, no_api=True,
    replay_changed_rows=changed, max_per_user_ap_replay_sensitivity=sensitivity,
    folds=checks, visual_review=review))
feature = summary['feature']
value = 100 * feature['pooled_map']
low, high = 100 * feature['ci95_low'], 100 * feature['ci95_high']
with (REP / 'summary_ru.md').open('a', encoding='utf-8') as stream:
    stream.write(f'\nГрафик проверен визуально; 17 строк. Исходные файлы и результаты 16 методов не изменились. '
                 f'Повторный инференс: перестановки top-12 в {changed} строках; '
                 f'максимальное изменение пользовательского AP={sensitivity:.10g}.\n')
with (ROOT / 'CONTEXT.md').open('a', encoding='utf-8') as stream:
    stream.write(f'\n\n## FEATURE: test-график всех методов (2026-10-19)\n\n'
        f'По запросу пользователя проверены существующие validation-selected FEATURE checkpoints '
        f'без обучения и переотбора. Run `{frozen["run_id"]}`. Те же три medium-v2 test-среза, '
        f'5519 наблюдений / 4548 исходных покупателей, каталог 10000. '
        f'Полный test MAP@12, включая недоступные цели: **{value:.4f}%**, '
        f'95% customer-bootstrap CI [{low:.4f}%; {high:.4f}%] (5000 повторов, seed42). '
        f'По фолдам: ' + ' / '.join(f'{100*x:.4f}%' for x in feature['fold_maps']) + '. '
        f'Reload: {changed} строк с изменением top-12, максимальная чувствительность AP={sensitivity:.10g}. '
        f'Новый график: `reports/medium_all_methods_h011_feature_v1/comparison_all.png`; '
        f'17 методов, все 16 прежних строк и исходный график сохранены. '
        f'FEATURE fanout64/32 + восемь categorical-кодов, без RHS ID lookup; исходный CE. '
        f'Старый ContextGNN corrected имеет иные fanout/типы признаков, поэтому это не чистая '
        f'FEATURE/FUSION абляция. Один seed и ранее просмотренные test-недели: внутреннее сравнение. '
        f'Визуальная проверка и контроль SHA завершены; подробности в summary_ru.md и final_verification.json.\n')
record('feature_all_methods_plot_complete',
    f'Frozen FEATURE test MAP@12={value:.4f}% (95% CI {low:.4f}..{high:.4f}%). '
    f'Chart visually verified with 17 methods, all original 16 rows/files unchanged. '
    f'No fitting/reselection/API. Reload changed {changed} top12 rows, max per-user AP sensitivity {sensitivity:.10g}.',
    frozen['run_id'], status=status, test_metrics={'map':feature['pooled_map']},
    artifacts=str(REP.relative_to(ROOT)), replay_changed_rows=changed,
    max_per_user_ap_replay_sensitivity=sensitivity)
print(status, feature)
