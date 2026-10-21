"""Provisional ordinary-ranking results while independent CPU inference finishes."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'CVFollowup'))
import novelty_audit as a
from common import read,write
import numpy as np

def main():
    rows=[]
    for key in ['contextgnn','contextgnn_old','idgnn','recformer_zero','recformer_tuned','manual','h008_20','h009_40']:
        acc={mode:[] for mode in ['normal','new_only']}
        ready=all((a.DEST/f'fold_{f}'/key/'verification.json').exists() for f in range(3))
        for f in range(3):
            annotation=read(a.DEST/f'fold_{f}/annotations.json')
            for mode in ['normal','new_only'] if ready else ['normal']:
                pred=np.load(a.methods(f)[key]['prediction'] if mode=='normal' else a.DEST/f'fold_{f}'/key/'new_predictions.npy')
                for p,t in zip(pred,annotation):
                    m=a.per_user(p,t)
                    acc[mode].append(dict(ap=m['all']['map'],repeat_ap=m['repeat']['ap_contribution'],
                        recall=m['new']['recall'],available_recall=m['new']['available_recall']))
        for mode,values in acc.items():
            if not values:continue
            ap=np.mean([v['ap'] for v in values]);r=np.mean([v['repeat_ap'] for v in values])
            rows.append(dict(method=key,mode=mode,map=float(ap),repeat_ap_fraction=float(r/ap) if ap else None,
                new_recall=float(np.mean([v['recall'] for v in values if v['recall'] is not None])),
                available_new_recall=float(np.mean([v['available_recall'] for v in values if v['available_recall'] is not None]))))
    write(a.REP/'preview.json',dict(provisional=True,rows=rows))
    print(rows,flush=True)

if __name__=='__main__':main()
