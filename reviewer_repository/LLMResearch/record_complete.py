"""Record completion after human-facing visual review of the H010 artifacts."""
from common import REPORT, RUN, read, write, record

result = read(REPORT / 'comparison.json')
done = read(REPORT / 'complete.json')
assert done['all60_accepted'] and done['full_replays'] and done['exact_dialog_audits']
done.update(status='complete', visual_review_passed=True)
write(REPORT / 'complete.json', done)
write(REPORT / 'pipeline_status.json', {'status': 'complete'})
record('h010_completed_verified',
       'H010 completed: all60 accepted programs, frozen selections, full replays, independent AP and exact dialog audits passed. Comparison/search figures visually reviewed. Pooled test MAP H0100.4291% vs H0090.4514%; difference -0.0224pp, paired95%CI[-0.1327,+0.0880]pp; no demonstrated improvement. H011 remains deferred by user.',
       RUN, status='complete', test_metrics={'map': result['methods']['h010']['pooled_map']},
       comparison=result, artifacts=str(REPORT.relative_to(REPORT.parents[1])), visual_review_passed=True)
