"""Correct datetime resolution in isolated GNN runs; retain historical failure."""
import argparse
import fcntl
import shutil
import subprocess
import sys
from common import ROOT,OLD,OUT,REPORT,read,write,sha,freeze_text,record

def build(fold,existing=False):
    name='gnn_timefix_existing' if existing else 'gnn_timefix_refit'
    folder=OUT/f'fold_{fold}'/name
    runtime=OUT/f'fold_{fold}/runtime'/name;runtime.mkdir(parents=True,exist_ok=True)
    source=OLD/f'fold_{fold}/runtime/gnn.py'
    code=source.read_text(encoding='utf-8')
    before='table.df.timestamp.astype("int64").to_numpy()//1_000_000_000'
    assert before in code
    code=code.replace(before,'unix_seconds(table.df.timestamp)')
    code=code.replace('import numpy as np','import numpy as np\nfrom time_units import unix_seconds')
    code=code.replace(f'OUT = Path({str(OLD/f"fold_{fold}/gnn")!r})',f'OUT = Path({str(folder)!r})')
    code=code.replace(f'hm_medium_cv_v2_fold{fold}_',f'hm_medium_followup_f{fold}_{name}_')
    # Record and assert actual context, in addition to the old future-node check.
    code=code.replace('    def validate_time(batch):',
         "    sampling_audit=[]\n    def validate_time(batch):\n        seed=batch[task.src_entity_table].seed_time\n        assert int(seed.min())>1_000_000_000, 'Cutoff was not converted to epoch seconds'\n        sampling_audit.append({'roots':int(batch[task.src_entity_table].batch_size),'article_nodes':int(batch[task.dst_entity_table].num_nodes),'cutoff_min':int(seed.min()),'cutoff_max':int(seed.max())})\n        (OUT/'sampling_audit.json').write_text(json.dumps(sampling_audit))")
    freeze_text(runtime/'gnn.py',code)
    for filename in ['cv_graph.py']:
        freeze_text(runtime/filename,(OLD/f'fold_{fold}/runtime'/filename).read_text(encoding='utf-8'))
    freeze_text(runtime/'time_units.py',(ROOT/'CVFollowup/time_units.py').read_text(encoding='utf-8'))
    if existing:
        for kind in ['idgnn','contextgnn']:
            dest=folder/kind;dest.mkdir(parents=True,exist_ok=True)
            if not(dest/'best.pt').exists():shutil.copyfile(OLD/f'fold_{fold}/gnn'/kind/'best.pt',dest/'best.pt')
            assert sha(dest/'best.pt')==sha(OLD/f'fold_{fold}/gnn'/kind/'best.pt')
    write(runtime/'provenance.json',{'source_sha256':sha(source),'runtime_sha256':sha(runtime/'gnn.py'),
          'only_model_input_fix':'normalize datetime resolution before epoch-seconds conversion',
          'same_checkpoint_diagnostic':existing,'fold':fold})
    return folder,runtime/'gnn.py'

def run(fold,stage):
    existing=stage=='existing'
    folder,runtime=build(fold,existing)
    flags={'existing':['--evaluate-only','--verify-only'],'train':['--train-only'],
           'evaluate':['--evaluate-only','--verify-only']}[stage]
    if stage=='train' and all((folder/k/'trained.json').exists() for k in ['idgnn','contextgnn']):return
    if stage in ['existing','evaluate'] and (folder/'verification.json').exists():
        assert read(folder/'verification.json')['passed'];return
    if stage=='train':assert read(REPORT/'graph_time_fix_verification.json')['passed']
    if stage=='evaluate':assert (REPORT/'gnn_timefix_pretest_freeze.json').exists()
    lockfolder=OUT/'locks';lockfolder.mkdir(parents=True,exist_ok=True)
    with (lockfolder/'gpu.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for flag in flags:
            if flag=='--evaluate-only' and all((folder/k/'metrics.json').exists() for k in ['idgnn','contextgnn']):continue
            subprocess.run([sys.executable,'-u',str(runtime),flag],cwd=ROOT,check=True)
    if stage=='existing':
        checks=read(folder/'sampling_audit.json')
        assert sum(x['article_nodes'] for x in checks)>0,'Time fix did not restore graph history'
        record('followup_gnn_timefix_existing',f'Fold{fold}: identical old GNN weights evaluated with corrected cutoffs; temporal context restored; diagnostic only because old checkpoint selection was faulty.',
               f'hm_medium_gnn_timefix_existing_f{fold}_v1',status='diagnostic_complete',artifacts=str(folder.relative_to(ROOT)))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('fold',type=int)
    parser.add_argument('stage',choices=['existing','train','evaluate'])
    args=parser.parse_args();run(args.fold,args.stage)
