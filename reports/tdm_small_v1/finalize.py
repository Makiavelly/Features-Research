"""Record completion after independent replay, artifact audit, and human-readable visual QA."""
import json
from pathlib import Path
import shutil
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record

out=ROOT/'TDM/results/hm_small_v1'
dest=ROOT/'reports/tdm_small_v1'
assert (ROOT/'TDM/logs/small_v1/pipeline.exitcode').read_text().strip()=='0'
assert json.loads((out/'verification.json').read_text())['passed']
assert json.loads((dest/'final_audit.json').read_text())['passed']
report=json.loads((dest/'report.json').read_text())
snapshot=out/'source'
snapshot.mkdir(exist_ok=True)
for p in (ROOT/'TDM').iterdir():
    if p.is_file() and p.suffix in ['.py','.sh','.md']:
        shutil.copyfile(p,snapshot/p.name)
summary=('Completed both authorized TDM small-v1 experiments. Fixed tree:7epochs,best3, '
         'beam val/test1.016010/1.395195 percent; exhaustive same checkpoint0.934150/1.002919 percent. '
         'Cluster tree:6epochs,best2,beam0.745875/0.551263 percent; exhaustive0.672455/0.466389 percent. '
         'Train+validation188.61s and132.85s; clustering13.29s; peak allocated CUDA102302720bytes each. '
         'Both selections fixed before test. All8 independent replays exact, final artifact audit passed, '
         'all3 PNGs visually checked, pipeline exit0. Local adaptation,one seed250testusers; '
         'cluster-minus-fixed beam bootstrap95 percent interval[-2.14275,+0.21911]pp, '
         'so robust general harm/benefit not established. Single-pass beam test7.86/7.18s versus '
         'full5.49/5.26s despite986/988 versus5000 scored nodes per user. '
         'No package/environment changes; earlier results preserved. Source snapshot retained.')
report['final']=True
report['visual_qa']={'passed':True,'reviewed':['comparison.png','learning_curves.png','search_cost.png']}
report['final_audit']=json.loads((dest/'final_audit.json').read_text())
report['summary']=summary
(dest/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=dest/'report.md'
text=path.read_text(encoding='utf-8')
lead=('\nFixed-tree TDM beam obtained test MAP@12=1.395195%; after embedding clustering it was0.551263%. '
      'The cluster-minus-fixed paired-user95% interval is[-2.14275;+0.21911]percentage points: '
      'these point results do not establish a stable effect across users or training seeds. '
      'ContextGNN and Recformer LR/warmup reference test MAPs are3.015575% and3.857513%.\n')
text=text.replace('\n\n','\n'+lead+'\n',1)
text+=('\nFinal artifact audit passed; all3 PNGs visually reviewed. The maximum difference between '
       'scores of beam-visited leaves and exhaustive scoring was below1e-6. All independent '
       'same-mode replays matched exactly.\n\nTiming clarification: the chart uses one pass with an already loaded model; '
       'there was no explicit warmup before every mode or repeated timing benchmark. '
       'This is an observed execution-time comparison, not a robust hardware speed benchmark.\n\n'
       'Frozen source copies retained under TDM/results/hm_small_v1/source/.\n')
path.write_text(text,encoding='utf-8')
for variant in ['fixed','cluster']:
    metrics=json.loads((out/variant/'beam/metrics.json').read_text())
    train=json.loads((out/variant/'training_summary.json').read_text())
    record('tdm_complete','TDM weekly run complete; independent replay and visual report checks passed',
           f'hm_tdm_small_{variant}_seed42_v1',status='complete',epoch=train['epochs'],
           val_metrics={'map':metrics['val_metrics']['map']},test_metrics={'map':metrics['test_metrics']['map']},
           artifacts=f'TDM/results/hm_small_v1/{variant}',summary=train)
record('tdm_pipeline_complete',summary,'hm_tdm_small_pipeline_v1',status='complete',
       artifacts='reports/tdm_small_v1',verification='TDM/results/hm_small_v1/verification.json',
       final_audit='reports/tdm_small_v1/final_audit.json')
print(summary)
