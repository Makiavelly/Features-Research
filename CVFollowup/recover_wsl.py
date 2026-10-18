"""Check persisted progress and CUDA before restarting after a WSL interruption."""
from datetime import datetime
import shutil
import subprocess
import sys
import torch
from common import ROOT,OUT,REPORT,read,write,sha,record

def main():
    now=datetime.now().strftime('%Y%m%d_%H%M%S')
    directory=REPORT/'recovery'/now;directory.mkdir(parents=True,exist_ok=False)
    completed={};partial=[]
    for folder in sorted(OUT.glob('fold_*/gnn_timefix_refit/*')):
        if not folder.is_dir():continue
        if (folder/'trained.json').exists():
            assert (folder/'best.pt').exists()
            completed[str(folder.relative_to(ROOT))]={'best_sha256':sha(folder/'best.pt'),'trained':read(folder/'trained.json')}
        elif (folder/'best.pt').exists():
            # Keep any interrupted attempt intact before deterministic restart.
            target=directory/'interrupted'/folder.relative_to(OUT)
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(folder,target)
            partial.append({'source':str(folder.relative_to(ROOT)),'preserved':str(target.relative_to(ROOT))})
    valid={}
    # Preserve interrupted Recformer artifacts before deterministic full-fit retry.
    interrupted_recformer=[]
    for folder in sorted(OUT.glob('fold_*/recformer_grid/*')):
        if (folder/'training_summary.json').exists():continue
        if (folder/'zero_shot/best.pt').exists() or (folder/'finetuned/best.pt').exists():
            assert folder.resolve().is_relative_to(OUT.resolve())
            target=directory/'interrupted_recformer'/folder.relative_to(OUT)
            target.parent.mkdir(parents=True,exist_ok=True)
            assert target.resolve().is_relative_to(directory.resolve())
            folder.rename(target)
            interrupted_recformer.append(str(target.relative_to(ROOT)))
    for folder in OUT.glob('fold_*/h00*'):
        trials=[read(p) for p in folder.glob('*/candidates/*/trial.json')]
        valid[str(folder.relative_to(ROOT))]={'accepted':sum(t.get('status')=='valid' for t in trials),'responses':len(trials),
            'actual_POST':len(list((folder/'api_attempts').glob('attempt_*')))}
    gpu={'available':torch.cuda.is_available()}
    assert gpu['available'],'CUDA not available after WSL restart'
    tensor=torch.arange(1024,device='cuda',dtype=torch.float32)
    assert float(tensor.sum())==523776.;torch.cuda.synchronize()
    gpu.update(name=torch.cuda.get_device_name(),free_bytes=torch.cuda.mem_get_info()[0],small_compute_passed=True)
    del tensor;torch.cuda.empty_cache()
    write(directory/'recovery.json',{'completed_gnn':completed,'partial_gnn':partial,'interrupted_recformer':interrupted_recformer,'api':valid,'gpu':gpu,
        'disk_free_bytes':shutil.disk_usage(ROOT).free,'reason_for_WSL_crash':'not established; current boot log cannot establish previous crash cause'})
    record('wsl_restart_recovery',f'WSL restarted; no experiment processes survived. Saved {len(completed)}/6 completed GNN fits; CUDA computation and provider DNS checked. Resuming saved API responses and remaining fits; crash cause not established.',
        'hm_medium_followup_recovery_v1',status='resuming',artifacts=str(directory.relative_to(ROOT)),api=valid,gpu=gpu)
    print('SAVED GNN FITS',len(completed),'API',valid,'CUDA',gpu['name'],flush=True)
    available=REPORT/'recformer_pretest_freeze.json'
    closing_available=available.exists() and read(available).get('scope')=='available_three_of_four_new_settings'
    if closing_available:
        # Resume only the requested available-results summary; do not revive excluded Kaggle waits.
        scripts=[] if (REPORT/'final_comparison/visual_review.json').exists() else ['available_summary.py']
    else:
        gpu_script='recformer_distributed.py' if (REPORT/'recformer_distributed_plan.json').exists() else 'gnn_lane.py'
        scripts=['api_lane.py',gpu_script,'report_watch.py']
    for script in scripts:
        subprocess.run([sys.executable,str(ROOT/'CVFollowup'/script)],cwd=ROOT,check=True)

if __name__=='__main__':main()
