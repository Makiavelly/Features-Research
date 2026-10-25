"""Independent stdlib-only checks. No training, model imports, network or API calls."""
from pathlib import Path
import collections,csv,gzip,hashlib,json,math
ROOT=Path(__file__).resolve().parent

def main():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text(encoding='utf8'))
    for rel,expected in manifest['files'].items():
        assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==expected,rel
    refs={}
    with (ROOT/'evidence/metrics_all_methods.csv').open(encoding='utf8',newline='') as f:
        for r in csv.DictReader(f):refs[r['method'],r['mode'],r['group']]=r
    aggregate=collections.defaultdict(lambda:collections.defaultdict(list));aps={};eligibility={}
    with gzip.open(ROOT/'evidence/per_user_metrics.csv.gz','rt',encoding='utf8',newline='') as f:
        for r in csv.DictReader(f):
            k=r['method'],r['mode'],r['group']
            for metric in ['map','available_recall','ap_contribution']:
                value=r[metric]
                if value and math.isfinite(float(value)):aggregate[k][metric].append(float(value))
            if r['mode']=='normal' and r['group']=='all':aps[r['method'],int(r['fold']),int(r['row'])]=float(r['map'])
            if r['group']=='new':
                who=int(r['fold']),int(r['row'])
                available=int(r['available'])>0
                assert eligibility.setdefault(who,available)==available
    checked=0
    for k,metrics in aggregate.items():
        ref=refs[k]
        for metric,column in [('map','map'),('available_recall','available_macro_recall'),('ap_contribution','ap_contribution')]:
            values=metrics[metric]
            if not values:continue
            actual=math.fsum(values)/len(values)
            assert abs(actual-float(ref[column]))<1e-12,(k,metric,actual,ref[column])
            checked+=1
        if k[2]=='all':assert len(metrics['map'])==5519
        if k[2]=='new':assert len(metrics['available_recall'])==3178
    with gzip.open(ROOT/'evidence/ranking_replay.json.gz','rt',encoding='utf8') as f:rankings=json.load(f)
    replay=collections.defaultdict(list)
    for r in rankings:
        pred=r['prediction'];targets=set(r['targets'])
        assert len(pred)==len(set(pred))==12 and all(0<=p<10000 for p in pred)
        assert targets
        hits=0;precision=[]
        for rank,item in enumerate(pred,1):
            if item in targets:hits+=1;precision.append(hits/rank)
        ap=math.fsum(precision)/min(12,len(targets))
        assert abs(ap-aps[r['method'],r['fold'],r['row']])<1e-12
        replay[r['method']].append(ap)
    for method,values in replay.items():
        assert len(values)==5519
        assert abs(math.fsum(values)/len(values)-float(refs[method,'normal','all']['map']))<1e-12
    assert len({k[0] for k in refs})==21 and sum(eligibility.values())==3178
    result={'passed':True,'files_verified':len(manifest['files']),'methods':21,'aggregate_values_checked':checked,'actual_top12_replays':len(rankings),'raw_prediction_methods':sorted(replay),'user_weeks_per_method':5519,'eligible_new_user_weeks':3178,'model_inference':False,'training':False,'api_requests':0}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
