"""Portable train-only runner for two predeclared Recformer grid settings."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import zipfile

def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def dump(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');tmp.replace(path)

def verify(root):
    manifest=json.loads((root/'input_manifest.json').read_text())
    for name,info in manifest['files'].items():
        file=root/name
        assert file.is_file() and file.stat().st_size==info['bytes'] and sha(file)==info['sha256'],name
    return manifest

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',required=True);parser.add_argument('--output',required=True)
    parser.add_argument('--label',choices=['lr3e6_w100','lr1e5_w300'],required=True)
    parser.add_argument('--check-only',action='store_true');args=parser.parse_args()
    root=Path(args.input).resolve();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    manifest=verify(root)
    provenance={'label':args.label,'input_manifest_sha256':sha(root/'input_manifest.json'),
        'protocol':'hm_medium_recformer_kaggle_split_v1','seed':42,'input_folds':manifest['folds'],
        'selection':'train only, choose checkpoint on existing inner validation; global selection after import locally',
        'versions':{n:importlib.metadata.version(n) for n in ['torch','transformers','tokenizers','numpy','pandas','pyarrow']},
        'python':platform.python_version(),'runtime_sha256':sha(Path(__file__)),
        'cross_hardware_note':'Same algorithm/data/hyperparameters, different GPU. AMP skipped updates/numerics may differ.'}
    dump(out/'run_manifest.json',provenance)
    if args.check_only:
        sys.path[:0]=[str(root/'RelBenchGNN/upstream'),str(root/'Recformer/upstream')]
        from relbench import load_dataset
        for fold in range(3):
            task=load_dataset(root/f'data/hm-cv-medium-v2/fold_{fold}').load_task('user-item-purchase')
            for split in ['train','val']:
                table=task.get_table(split,mask_input_cols=False)
                assert len(table.df)==manifest['folds'][str(fold)][split+'_rows']
        print('INPUT AND TABLE PREFLIGHT PASSED',flush=True);return
    import torch
    assert torch.cuda.is_available(),'Enable GPU T4 in Kaggle notebook settings'
    provenance['gpu']=torch.cuda.get_device_name();provenance['cuda']=torch.version.cuda
    dump(out/'run_manifest.json',provenance)
    env=os.environ.copy();env['RECFORMER_BUNDLE_ROOT']=str(root);env['RECFORMER_KAGGLE_OUT']=str(out)
    env['PYTHONPATH']=os.pathsep.join([str(root/'RelBenchGNN'),str(root/'RelBenchGNN/upstream')])
    completed=[]
    try:
        for fold in range(3):
            folder=out/f'fold_{fold}/recformer_grid'/args.label
            if (folder/'training_summary.json').exists():
                print('REUSE COMPLETED FOLD',fold,flush=True)
            else:
                assert not(folder/'finetuned/best.pt').exists(),'Partial training exists: preserve it and use a new output directory; optimizer/RNG resume is not implemented'
                source=root/f'runtime/fold_{fold}/recformer_{args.label}.py'
                print('TRAIN',args.label,'fold',fold,flush=True)
                with (out/f'fold_{fold}_{args.label}.log').open('a',buffering=1) as log:
                    process=subprocess.Popen([sys.executable,'-u',str(source),'--variant','low_lr_warmup','--train-only'],
                        env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
                    for line in process.stdout:print(line,end='',flush=True);log.write(line)
                    assert process.wait()==0,f'Fold{fold} failed; see output log'
            summary=json.loads((folder/'training_summary.json').read_text())
            config=json.loads((folder/'config.json').read_text())
            assert summary['epochs']==4 and config['batch']==4 and config['gradient_accumulation']==4
            expected=manifest['settings'][args.label]
            assert config['lr']==expected['peak_lr'] and config['warmup_updates']==expected['warmup']
            # Ship only the selected trained checkpoint, not the identical epoch0 copy.
            artifacts={}
            for path in folder.iterdir():
                if path.is_file() and path.suffix in ['.json','.jsonl']:artifacts[str(path.relative_to(out))]=sha(path)
            artifacts[str((folder/'finetuned/best.pt').relative_to(out))]=sha(folder/'finetuned/best.pt')
            completed.append({'fold':fold,'summary':summary,'artifacts':artifacts})
            dump(out/'completed_folds.json',completed)
    finally:
        # Partial reports remain downloadable through Save Version, even on a Python error.
        archive=out.parent/f'{out.name}_results.zip'
        files=[p for p in out.rglob('*') if p.is_file() and (p.suffix in ['.json','.jsonl','.log'] or p.name=='best.pt' and p.parent.name=='finetuned')]
        digests={str(p.relative_to(out)):sha(p) for p in files}
        dump(out/'export_manifest.json',{'label':args.label,'input_manifest_sha256':provenance['input_manifest_sha256'],
            'files':digests,'completed_folds':len(completed),'test_evaluated':False})
        with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_STORED) as z:
            for p in [*files,out/'export_manifest.json']:z.write(p,str(p.relative_to(out)))
        print('RESULT ZIP:',archive,flush=True)

if __name__=='__main__':main()
