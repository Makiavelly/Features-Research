"""Validate remote result archive and import completed grid fits without overwrites."""
import argparse
import json
import math
import os
from pathlib import Path
import shutil
import zipfile
from common import ROOT,OLD,OUT,REPORT,read,write,sha,record

def main():
    p=argparse.ArgumentParser();p.add_argument('archive');args=p.parse_args()
    archive=Path(args.archive).resolve();digest=sha(archive)
    extracted=OUT/'imports'/digest
    extracted.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();assert len(names)==len(set(names))
        for name in names:
            assert (extracted/name).resolve().is_relative_to(extracted.resolve()) and not name.startswith('/'),'Unsafe ZIP member'
        z.extractall(extracted)
    export=read(extracted/'export_manifest.json');run=read(extracted/'run_manifest.json')
    expected=read(ROOT/'CVFollowup/kaggle/bundle_manifest.json')
    assert export['input_manifest_sha256']==run['input_manifest_sha256']==expected['input_manifest_sha256']
    label=export['label'];assert label==run['label'] and label in ['lr3e6_w100','lr1e5_w300']
    assert export['completed_folds']==3 and not export['test_evaluated']
    for name,value in export['files'].items():assert sha(extracted/name)==value,name
    inputs=read(ROOT/'CVFollowup/cache/kaggle_recformer_v1/input_manifest.json')
    checkpoints=[]
    for fold in range(3):
        rel=Path(f'fold_{fold}/recformer_grid')/label;source=extracted/rel
        cfg=read(source/'config.json');summary=read(source/'training_summary.json');history=read(source/'history.json')
        setting=inputs['settings'][label]
        assert cfg['lr']==setting['peak_lr'] and cfg['warmup_updates']==setting['warmup']
        assert cfg['seed']==42 and cfg['batch']==4 and cfg['gradient_accumulation']==4
        assert cfg['epochs_per_stage']==2 and cfg['stages']==2 and cfg['max_tokens']==256 and cfg['max_items']==50
        assert cfg['subset_sha256']==inputs['folds'][str(fold)]['subset_sha256']
        assert cfg['pretrained_sha256']==inputs['files']['data/models/recformer/recformer_seqrec.bin']['sha256']
        assert cfg['runner_sha256']==inputs['files'][f'runtime/fold_{fold}/recformer_{label}.py']['sha256']
        assert cfg['runtime']['torch']=='2.2.2+cu118' and cfg['runtime']['transformers']=='4.46.3'
        assert [(h['stage'],h['epoch']) for h in history]==[(1,1),(1,2),(2,1),(2,2)]
        assert summary['epochs']==4 and all(math.isfinite(h['val_metrics']['map']) for h in history)
        assert summary['best_trained_val_map']==max(h['val_metrics']['map'] for h in history)
        assert (source/'finetuned/best.pt').stat().st_size>100_000_000
        assert read(source/'frozen_verification.json')['passed']
        checkpoints.append((fold,rel,source))
    # Validate ALL folds before mutating any grid result directory.
    for fold,rel,source in checkpoints:
        dest=OUT/rel
        if (dest/'external_import.json').exists():
            assert read(dest/'external_import.json')['archive_sha256']==digest;continue
        assert not(dest/'finetuned/best.pt').exists() and not(dest/'training_summary.json').exists(),'Refuse to overwrite training'
        dest.mkdir(parents=True,exist_ok=True)
        for file in source.rglob('*'):
            if file.is_file():
                target=dest/file.relative_to(source);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(file,target)
        # Epoch0 is a shared frozen control. Reuse its local checkpoint only for evaluator compatibility.
        zero=dest/'zero_shot';zero.mkdir(exist_ok=True)
        frozen=OLD/f'fold_{fold}/recformer/zero_shot/best.pt'
        if not(zero/'best.pt').exists():
            try:os.link(frozen,zero/'best.pt')
            except OSError:shutil.copyfile(frozen,zero/'best.pt')
        assert sha(zero/'best.pt')==sha(frozen)
        write(dest/'external_import.json',{'archive_sha256':digest,'source_run':run,
            'checkpoint_sha256':sha(dest/'finetuned/best.pt'),'zero_control':'reused existing frozen local baseline epoch0; remote trained checkpoint retained unchanged'})
    record('recformer_kaggle_imported',f'Imported three verified Kaggle folds for {label}; no outer evaluation; immutable archive retained. GPU provenance preserved.',
        f'hm_medium_recformer_import_{label}_v1',status='trained_pending_selection',archive_sha256=digest)
    print('IMPORTED',label,'3 folds',flush=True)

if __name__=='__main__':main()
