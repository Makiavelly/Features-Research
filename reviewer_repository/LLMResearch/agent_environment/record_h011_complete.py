"""Close the verified H011 report after visual review; never refit or reselect."""
from h011_stage import ROOT, OUT, REPORT, RUN, read, write, record, sha

result = read(REPORT / 'comparison.json')
done = read(REPORT / 'complete.json')
assert done['all60_accepted'] and done['full_replays']
frozen = read(REPORT / 'pretest_freeze.json')
for fold in range(3):
    folder = OUT / f'fold_{fold}'
    assert read(folder / 'verification.json')['passed']
    assert len(read(folder / 'budget.json')['accepted']) == 20
    assert read(folder / 'test_metrics.json')['map'] == result['folds'][fold]['h011_map']
    assert read(folder / 'selected.json')['program_sha256'] == frozen['folds'][str(fold)]['program_sha256']
summary = REPORT / 'summary_ru.md'
text = summary.read_text(encoding='utf-8')
text = text.replace('График требует визуальной проверки перед окончательным закрытием эксперимента.',
                    'График просмотрен; итоговая визуальная проверка пройдена.')
if 'Изменение бюджета во время поиска' not in text:
    rows = ['Фолд | Test MAP@12 | Исследовательские вызовы | API POST', '---|---:|---:|---:']
    rows += [f"{r['fold']}|{r['h011_map']*100:.4f}%|{r['research_requests']}|{r['actual_POST']}" for r in result['folds']]
    text += '\n' + '\n'.join(rows) + '\n\n'
    text += ('Изменение бюджета во время поиска: после14 принятых программ фолда0 пользователь увеличил '
             'исследовательский лимит40 до300/фолд (100/популяцию). Продолжены прежние разговоры, '
             'программы и счётчики; это продолжение с изменённым протоколом, не независимый перезапуск. '
             'Исходное состояние сохранено в reports/medium_h011_codex_v1/before_budget300/.\n\n')
    text += (f"Всего{sum(r['research_requests'] for r in result['folds'])} исследовательских вызова,"
             f"{sum(r['actual_POST'] for r in result['folds'])} API POST. Известные входные токены:"
             f"{result['known_input_tokens']} (включают историю/кеш), выходные:{result['known_output_tokens']}. "
             f"Неизвестный usage у{result['unknown_usage_attempts']} попыток. "
             'Парный интервал разницы включает ноль; улучшение относительно H009 не подтверждено.\n')
summary.write_text(text, encoding='utf-8')
done.update(status='complete', visual_review_passed=True, independent_AP=True)
write(REPORT / 'complete.json', done)
write(REPORT / 'pipeline_status.json', {'status': 'complete'})
record('h011_completed_verified',
       'H011 autonomous Codex completed:60 accepted programs, all selections frozen before outer scoring, full replays and independent AP verified; comparison figure visually reviewed. Pooled test MAP0.4307% vs H0090.4514%; difference-0.0207pp, paired95%CI[-0.1445,+0.1073]pp. Folds0.1952%,0.6795%,0.3955%.84 research calls,445 API POST. No demonstrated improvement; budget40-to300 revision/inherited state retained in provenance.',
       RUN, status='complete', test_metrics={'map': result['h011_pooled_map']},
       comparison=result, visual_review_passed=True, artifacts=str(REPORT.relative_to(ROOT)))
