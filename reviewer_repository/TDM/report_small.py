"""Report from frozen predictions; no training or checkpoint selection."""
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import ROOT,OUT,CONFIG,Dataset,ap_per_user,dump,sha,record

DEST=ROOT/'reports/tdm_small_v1'

def bootstrap(a,b):
    delta=a-b
    rng=np.random.default_rng(42)
    means=delta[rng.integers(0,len(delta),(10000,len(delta)))].mean(1)*100
    return dict(difference_pp=float(delta.mean()*100),paired_user_bootstrap95_pp=np.quantile(means,[.025,.975]).tolist())

def main():
    assert json.loads((OUT/'verification.json').read_text())['passed']
    dataset=Dataset()
    DEST.mkdir(exist_ok=True)
    rows=[];aps={}; results={}
    references=[('ID-GNN',ROOT/'ContextGNN/results/hm_small_v1/idgnn'),
                ('ContextGNN',ROOT/'ContextGNN/results/hm_small_v1/contextgnn'),
                ('Two-tower',ROOT/'ContextGNN/results/hm_small_v1/two_tower'),
                ('Manual LightGBM',ROOT/'ContextGNN/results/hm_small_v1/lightgbm_manual'),
                ('ID-GNN -> LightGBM',ROOT/'ContextGNN/results/hm_small_v1/lightgbm_idgnn'),
                ('Recformer zero-shot',ROOT/'Recformer/results/hm_small_seed42_v1/zero_shot'),
                ('Recformer old fine-tuned',ROOT/'Recformer/results/hm_small_seed42_v1/finetuned'),
                ('Recformer LR/warmup',ROOT/'Recformer/results/hm_small_low_lr_warmup_seed42_v1/finetuned')]
    for label,folder in references:
        row={'model':label}
        aps[label]={}
        for split in ['val','test']:
            pred=np.load(folder/f'{split}_predictions.npy')
            assert pred.shape==(len(dataset.targets[split]),12)
            ap=ap_per_user(pred,dataset.targets[split])
            aps[label][split]=ap
            row[f'{split}_map_percent']=float(ap.mean()*100)
        rows.append(row)
    for variant in ['fixed','cluster']:
        summary=json.loads((OUT/variant/'training_summary.json').read_text())
        results[variant]={'summary':summary,'config':json.loads((OUT/variant/'config.json').read_text()),'modes':{}}
        for mode in ['beam','full']:
            label=f'TDM {variant} {mode}'
            row={'model':label}
            metric=json.loads((OUT/variant/mode/'metrics.json').read_text())
            results[variant]['modes'][mode]=metric
            aps[label]={}
            for split in ['val','test']:
                folder=OUT/variant/mode
                pred=np.load(folder/f'{split}_predictions.npy')
                ap=ap_per_user(pred,dataset.targets[split])
                assert np.array_equal(ap,np.load(folder/f'{split}_ap_per_user.npy'))
                assert abs(ap.mean()-metric[f'{split}_metrics']['map'])<1e-12
                aps[label][split]=ap
                row[f'{split}_map_percent']=float(ap.mean()*100)
            rows.append(row)
    comparisons={}
    for a,b in [('TDM cluster beam','TDM fixed beam'),('TDM fixed beam','TDM fixed full'),
                ('TDM cluster beam','TDM cluster full'),('TDM fixed beam','ContextGNN'),
                ('TDM cluster beam','ContextGNN'),('TDM fixed beam','Recformer LR/warmup'),
                ('TDM cluster beam','Recformer LR/warmup')]:
        comparisons[f'{a} minus {b}']=bootstrap(aps[a]['test'],aps[b]['test'])
    with (DEST/'comparison.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    for label,values in aps.items():
        if label.startswith('TDM'):
            with (DEST/(label.replace(' ','_')+'_test_user_ap.csv')).open('w',newline='') as f:
                writer=csv.writer(f);writer.writerow(['customer_id','timestamp','ap12'])
                writer.writerows(zip(dataset.tables['test'].df.customer_id,dataset.tables['test'].df.timestamp,values['test']))
    fig,axes=plt.subplots(1,2,figsize=(15,7),sharey=True)
    labels=[r['model'] for r in rows]
    colors=['#246a9b' if r['model'].startswith('TDM') else '#9ba8b1' for r in rows]
    for ax,split in zip(axes,['val','test']):
        vals=[r[f'{split}_map_percent'] for r in rows]
        ax.barh(labels,vals,color=colors)
        ax.set_xlim(0,max(vals)*1.24)
        for i,v in enumerate(vals):ax.text(v+.03,i,f'{v:.3f}',va='center',fontsize=9)
        ax.set_title(f'{split}: MAP@12 (%)');ax.grid(axis='x',alpha=.2)
    axes[0].invert_yaxis()
    fig.suptitle('Frozen H&M small-v1: 5000 items; 304 validation / 250 test users; seed42')
    fig.tight_layout();fig.savefig(DEST/'comparison.png',dpi=160);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    for variant in ['fixed','cluster']:
        hist=json.loads((OUT/variant/'history.json').read_text())
        ep=[x['epoch'] for x in hist]
        axes[0].plot(ep,[x['train_loss'] for x in hist],marker='.',label=variant)
        axes[1].plot(ep,[x['val_metrics']['map']*100 for x in hist],marker='.',label=variant)
    for ax in axes: ax.set_xlabel('Epoch');ax.legend();ax.grid(alpha=.2)
    axes[0].set_ylabel('Balanced weekly BCE');axes[1].set_ylabel('Validation beam64 MAP@12 (%)')
    fig.tight_layout();fig.savefig(DEST/'learning_curves.png',dpi=160);plt.close(fig)
    own=[r for r in rows if r['model'].startswith('TDM')]
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    ownlabels=[r['model'].replace('TDM ','') for r in own]
    metrics=[results[v]['modes'][m]['test_metrics'] for v in ['fixed','cluster'] for m in ['beam','full']]
    axes[0].bar(ownlabels,[x['seconds'] for x in metrics]);axes[0].set_ylabel('Test scoring seconds (warm, includes search)')
    axes[1].bar(ownlabels,[x['mean_scored_nodes'] for x in metrics]);axes[1].set_ylabel('Mean scored nodes per user')
    for ax in axes:ax.grid(axis='y',alpha=.2)
    fig.tight_layout();fig.savefig(DEST/'search_cost.png',dpi=160);plt.close(fig)
    lines=['# TDM: fixed and embedding-cluster trees on H&M small-v1','',
           'Both models were selected by beam64 validation MAP before either test evaluation.',
           'Local PyTorch adaptation of TDM; not unchanged TorchEasyRec and not JTM.',
           'Frozen4804train/304val/250test, full5000item candidate catalog, weekly multi-positive targets, one seed42.','',
           '| Model | Validation MAP, % | Test MAP, % |','|---|---:|---:|']
    for r in rows:lines.append(f"| {r['model']} | {r['val_map_percent']:.6f} | {r['test_map_percent']:.6f} |")
    lines+=['','![Comparison](comparison.png)','![Learning](learning_curves.png)','![Search cost](search_cost.png)','',
            '| TDM variant | Selected epoch | Epochs | Train+validation seconds | Peak CUDA GiB | Stop |',
            '|---|---:|---:|---:|---:|---|']
    for variant in results:
        s=results[variant]['summary']
        lines.append(f"| {variant} | {s['best_epoch']} | {s['epochs']} | {s['training_and_validation_seconds']:.2f} | {s['peak_cuda_bytes']/2**30:.3f} | {s['stop_reason']} |")
    lines+=['','Clustering prerequisite: '+json.dumps(json.loads((OUT/'cluster_provenance.json').read_text())),
            '', '| Test comparison | Difference, pp | Paired bootstrap95%, pp |','|---|---:|---|']
    for name,c in comparisons.items():lines.append(f"| {name} | {c['difference_pp']:+.5f} | {c['paired_user_bootstrap95_pp']} |")
    lines+=['','All8beam/full ×val/test independent replays match arrays, scores, traces, top12 and AP exactly.',
            'References are recomputed from frozen top12, not retrained. Old artifacts remain untouched.',
            'Full-leaf scoring uses the exact same selected checkpoint as beam; it is a diagnostic of routing, not another tuned model.',
            'Tree clustering uses the fixed model own train-learned leaf embeddings; clustered model retrains from scratch.',
            'Cluster total prerequisite cost includes fixed model training and clustering. Early stopping budgets can differ in realized epochs.',
            'No claim of general superiority:250testusers,one seed,different model/pretraining budgets. Bootstrap describes users, not training randomness.',
            'Native retrieval includes the full catalog as eligible leaves while evaluating a subset of nodes. Repeat purchases allowed.',
            'Warm inference times exclude environment/checkpoint initialization and data loading; no speed claim from node counts alone.',
            '', '[Protocol](../../TDM/PROTOCOL_SMALL.md) · [Research/provenance](../tdm_assessment/report.md)','']
    (DEST/'report.md').write_text('\n'.join(lines),encoding='utf-8')
    dump(DEST/'report.json',dict(comparison=rows,results=results,comparisons=comparisons,
         verification=json.loads((OUT/'verification.json').read_text()),
         plots={p.name:sha(p) for p in DEST.glob('*.png')}))
    record('tdm_report_ready','TDM measured and replay-verified; report prepared for visual review','hm_tdm_small_pipeline_v1',
           status='verified_pending_visual_review',artifacts='reports/tdm_small_v1',comparisons=comparisons)
    print(json.dumps(dict(comparison=rows,comparisons=comparisons)),flush=True)

if __name__=='__main__': main()
