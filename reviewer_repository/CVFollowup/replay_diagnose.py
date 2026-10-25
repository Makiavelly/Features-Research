"""Capture replay scores without modifying frozen GNN source or predictions."""
import subprocess
import sys
import numpy as np
from common import ROOT,OUT,REPORT,read,write,sha,freeze_text,record

def main():
    folder=OUT/'fold_2/gnn_timefix_refit'
    runtime=OUT/'fold_2/runtime/gnn_timefix_refit'
    source=runtime/'gnn.py';text=source.read_text(encoding='utf-8')
    needle='                scores_close = np.allclose(scores, old_scores, atol=1e-5, rtol=1e-5)'
    assert needle in text
    text=text.replace(needle,"                np.save(OUT / f'{kind}_{split}_diagnostic_replay.npy', scores)\n"+needle)
    text=text.replace('(OUT / "verification.json").write_text','(OUT / "diagnostic_verification.json").write_text')
    diagnostic=runtime/'gnn_replay_diagnostic.py';freeze_text(diagnostic,text)
    result=subprocess.run([sys.executable,'-u',str(diagnostic),'--verify-only'],cwd=ROOT)
    rows=[]
    for kind in ['idgnn','contextgnn']:
        for split in ['val','test']:
            a=np.load(folder/kind/f'{split}_scores.npy');b=np.load(folder/f'{kind}_{split}_diagnostic_replay.npy')
            finite=np.isfinite(a)&np.isfinite(b)
            diff=np.abs(a[finite].astype(np.float64)-b[finite].astype(np.float64))
            close=np.isclose(a,b,atol=1e-5,rtol=1e-5)
            rows.append({'model':kind,'split':split,'shape':list(a.shape),'failed_values':int((~close).sum()),
                'nan_saved':int(np.isnan(a).sum()),'nan_replay':int(np.isnan(b).sum()),
                'finite_pattern_equal':bool(np.array_equal(np.isfinite(a),np.isfinite(b))),
                'max_abs_difference':float(diff.max(initial=0)),
                'difference_quantiles':np.quantile(diff,[.5,.99,.999,1]).tolist() if len(diff) else [],
                'max_score_magnitude':float(np.max(np.abs(a[finite]),initial=0)),
                'saved_sha256':sha(folder/kind/f'{split}_scores.npy')})
    write(REPORT/'gnn_replay_score_diagnosis.json',{'returncode':result.returncode,'rows':rows})
    print(rows,flush=True)

if __name__=='__main__':main()
