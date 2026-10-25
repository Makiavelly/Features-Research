"""Fresh corrected medium reproduction, with a new namespace and pretest barrier.

Builds the original adapters and the original time fix, then changes only output
paths/run IDs. No API lane. Historical snapshots and model results are untouched.
"""
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'CVBenchmark'))
from build_runtime import build as build_original
sys.modules.pop('common',None)  # The historical script directories each define common.py.
sys.path.insert(0,str(ROOT/'CVFollowup'))
from gnn_timefix import build as build_corrected

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('stage',choices=['build','train','evaluate','verify'])
    p.add_argument('--run-name',default='reviewer_corrected_v1')
    a=p.parse_args();assert re.fullmatch(r'[A-Za-z0-9_-]+',a.run_name)
    dest=ROOT/'CVFollowup/results'/a.run_name
    jobs=[]
    for fold in range(3):
        build_original(fold)
        old,source=build_corrected(fold,False)
        folder=dest/f'fold_{fold}/gnn';runtime=dest/f'fold_{fold}/runtime'
        runtime.mkdir(parents=True,exist_ok=True)
        code=source.read_text(encoding='utf8')
        old_out=f'OUT = Path({str(old)!r})';assert old_out in code
        code=code.replace(old_out,f'OUT = Path({str(folder)!r})')
        old_id=f'hm_medium_followup_f{fold}_gnn_timefix_refit_';assert old_id in code
        code=code.replace(old_id,f'{a.run_name}_f{fold}_')
        for name,value in [('gnn.py',code)]+[(n,(source.parent/n).read_text(encoding='utf8')) for n in ['cv_graph.py','time_units.py']]:
            target=runtime/name;compile(value,str(target),'exec')
            if target.exists():assert target.read_text(encoding='utf8')==value,'Changed runtime: choose a new --run-name'
            else:target.write_text(value,encoding='utf8')
        jobs.append((folder,runtime/'gnn.py'))
    if a.stage=='build':
        print('PASS: three corrected runtimes built; no model imports, training, inference or API calls');return
    freeze=dest/'pretest_freeze.json'
    if a.stage=='train':
        assert not freeze.exists(),'Selection already frozen; use a new run name for another training'
        for folder,script in jobs:
            subprocess.run([sys.executable,'-u',str(script),'--train-only'],cwd=ROOT,check=True)
        refs={}
        for folder,script in jobs:
            for kind in ['idgnn','contextgnn']:
                for name in ['best.pt','trained.json']:
                    path=folder/kind/name;refs[path.relative_to(ROOT).as_posix()]=digest(path)
            for path in script.parent.glob('*.py'):refs[path.relative_to(ROOT).as_posix()]=digest(path)
        freeze.write_text(json.dumps({'run_name':a.run_name,'all_selections_finished_before_outer_scoring':True,'references':refs},indent=2),encoding='utf8')
        print('All six fits finished; pretest hashes frozen. Evaluation has not run.');return
    assert freeze.exists(),'Train all three folds and freeze selection before outer evaluation'
    record=json.loads(freeze.read_text(encoding='utf8'))
    for rel,expected in record['references'].items():assert digest(ROOT/rel)==expected,rel
    for folder,script in jobs:
        flag='--evaluate-only' if a.stage=='evaluate' else '--verify-only'
        subprocess.run([sys.executable,'-u',str(script),flag],cwd=ROOT,check=True)

if __name__=='__main__':main()
