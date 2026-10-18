"""Frozen LR/warmup grid using the existing model/data/objective implementation."""
import argparse
import fcntl
from pathlib import Path
import shutil
import subprocess
import sys
from common import ROOT,OLD,OUT,REPORT,read,write,sha,freeze_text,record

GRID={'lr1e6_w100':(1e-6,100),'lr3e6_w100':(3e-6,100),
      'lr1e5_w300':(1e-5,300),'lr3e6_w300':(3e-6,300)}

def build(fold,label):
    lr,warmup=GRID[label]
    source=OLD/f'fold_{fold}/runtime/recformer.py'
    folder=OUT/f'fold_{fold}/recformer_grid'/label
    text=source.read_text(encoding='utf-8')
    oldout=OLD/f'fold_{fold}/recformer'
    changes=[(f'OUT=Path({str(oldout)!r})',f'OUT=Path({str(folder)!r})'),
        (f"RUN='hm_medium_cv_v2_fold{fold}_recformer'",f"RUN='hm_medium_recformer_tune_f{fold}_{label}_seed42_v1'"),
        ("learning_rate=1e-5 if args.variant=='low_lr_warmup' else 5e-5",f'learning_rate={lr!r}'),
        ('def lr_multiplier(update, total=1204, warmup=100):',f'def lr_multiplier(update, total=1204, warmup={warmup}):'),
        ("assert lr_multiplier(0)==.01 and lr_multiplier(99)==1 and lr_multiplier(1204)==0",
         f'assert abs(lr_multiplier(0)-1/{warmup})<1e-12 and lr_multiplier({warmup-1})==1 and lr_multiplier(1204)==0'),
        ("'scheduler':'100 successful optimizer updates warmup, then linear decay over1204 updates' if args.variant=='low_lr_warmup' else 'constant; same as original'",
         f"'scheduler':'{warmup} successful optimizer updates warmup, linear decay over fold-specific planned total'"),
        ("'warmup_updates':100 if args.variant=='low_lr_warmup' else 0",f"'warmup_updates':{warmup}, 'planned_total_updates':math.ceil(math.ceil(len(encoded['train'])/4)/4)*4"),
        ("'comparison_policy':'same pretrained initialization, seed/order/2+2 epochs; lower LR+schedule bundled; freezing separately versus original constant5e-5'",
         "'comparison_policy':'predeclared follow-up LR/warmup grid; identical pretrained weights, data, ordering,2+2epochs and stage2 behavior; select by inner validation only'")]
    for old,new in changes:
        assert old in text,old;text=text.replace(old,new)
    runtime=OUT/f'fold_{fold}/runtime/recformer_{label}.py'
    freeze_text(runtime,text)
    write(runtime.with_suffix('.provenance.json'),{'source':str(source),'source_sha256':sha(source),
          'runtime_sha256':sha(runtime),'peak_lr':lr,'warmup_updates':warmup,
          'dataset_manifest_sha256':sha(ROOT/f'data/hm-cv-medium-v2/fold_{fold}/subset_manifest.json')})
    return folder,runtime

def run(fold,label,stage):
    folder,runtime=build(fold,label)
    if stage=='train' and (folder/'training_summary.json').exists():return
    if stage=='evaluate':
        frozen=read(REPORT/'recformer_pretest_freeze.json')
        assert frozen['selected_label']==label,'Only validation-selected setting may use outer scoring'
        assert sha(folder/'finetuned/best.pt')==frozen['checkpoints'][str(fold)]
        if (folder/'verification.json').exists():assert read(folder/'verification.json')['passed'];return
    locks=OUT/'locks';locks.mkdir(parents=True,exist_ok=True)
    with (locks/'gpu.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        if stage=='train':
            assert shutil.disk_usage(ROOT).free>3.5*1024**3,'Insufficient free disk for preserved checkpoints'
            command=[sys.executable,'-u',str(runtime),'--variant','low_lr_warmup','--train-only']
            subprocess.run(command,cwd=ROOT,check=True)
        else:
            for flag in ['--evaluate-only','--verify-only']:
                if flag=='--evaluate-only' and (folder/'finetuned/metrics.json').exists():continue
                subprocess.run([sys.executable,'-u',str(runtime),'--variant','low_lr_warmup',flag],cwd=ROOT,check=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('fold',type=int)
    parser.add_argument('label',choices=list(GRID));parser.add_argument('stage',choices=['train','evaluate'])
    args=parser.parse_args();run(args.fold,args.label,args.stage)
