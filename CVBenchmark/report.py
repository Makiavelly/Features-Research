"""Paired cross-fold report: full targets, catalog diagnostic and user uncertainty."""
import itertools
import shutil
import subprocess
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import ROOT,DATA,OUT,REPORT,read,write,sha,save_predictions

METHODS={
    'manual':('LightGBM manual','lightgbm_manual'),
    'raw15':('LightGBM raw15','lightgbm_raw15'),
    'idgnn':('ID-GNN','gnn/idgnn'),
    'contextgnn':('ContextGNN','gnn/contextgnn'),
    'recformer_zero':('Recformer zero-shot','recformer/zero_shot'),
    'recformer_lr':('Recformer LR/warmup','recformer/finetuned'),
    'tdm':('TDM fixed beam64','tdm/fixed/beam'),
    'h008':('API GPT H008 best-only','h008'),
    'h009':('API GPT H009 full history','h009')}

def main():
    assert (REPORT/'selection_pretest.json').exists()
    assert read(REPORT/'saved_schema_verification.json')['status']=='passed'
    arrays=[];identities=[];foldids=[];rows=[];apirows=[];costs=[]
    for fold in range(3):
        data=DATA/f'fold_{fold}';out=OUT/f'fold_{fold}'
        for verified in ['gnn/verification.json','recformer/verification.json','tdm/fixed/beam/verification.json',
                         'lightgbm_manual/verification.json','lightgbm_raw15/verification.json',
                         'h008/verification.json','h009/verification.json']:
            assert read(out/verified)['passed'],f'Missing/failed replay: fold{fold} {verified}'
        target=pd.read_parquet(data/'bundle/test_targets.parquet')
        # Original IDs, not fold-local offsets, define bootstrap clusters.
        mapping=pd.read_csv(data/'customer_id_map.csv').set_index('customer_id').original_customer_id
        identities.extend(target.customer_id.map(mapping));foldids.extend([fold]*len(target));foldap=[]
        for key,(label,path) in METHODS.items():
            folder=out/path
            pred=np.load(folder/'test_predictions.npy')
            result=save_predictions(folder,'test',pred,target)
            foldap.append(np.load(folder/'test_ap.npy'))
            rows.append({'fold':fold,'method':key,'label':label,**result})
            if key in ['manual','raw15']:
                seconds=read(folder/'trained.json')['seconds']
            elif key in ['idgnn','contextgnn']:
                seconds=read(folder/'trained.json')['seconds']
            elif key=='tdm':seconds=read(out/'tdm/fixed/training_summary.json')['training_and_validation_seconds']
            elif key=='recformer_lr':seconds=read(out/'recformer/training_summary.json')['training_and_validation_seconds']
            elif key=='recformer_zero':seconds=0.
            else:seconds=read(folder/'trained.json')['seconds']
            costs.append({'fold':fold,'method':key,'training_or_search_seconds':seconds,
                          'note':'pretrained; item encoding and external pretraining excluded' if key=='recformer_zero' else 'native training/search timer; setup boundaries differ'})
            if key.startswith('h00'):
                cfg=read(folder/'run_config.json');trials=[read(p) for p in sorted((folder/cfg['arm']/'candidates').glob('*/trial.json'))]
                assert sum(t['status']=='valid' for t in trials)==20
                subprocess.run([sys.executable,str(ROOT/'CVBenchmark/audit_numeric.py'),str(fold),key],check=True)
                diversity=read(folder/'numeric_diversity.json');assert diversity['status']=='passed'
                sys.path.insert(0,str(out/'runtime/api'))
                from dialog_history import build_messages
                tokens=0;outputtokens=0
                for t in trials:
                    candidate=folder/cfg['arm']/'candidates'/f"candidate_{t['call']:03d}"
                    response=read(candidate/'response.json')
                    request=read(folder/'api_attempts'/f"attempt_{response['api_attempt']:03d}"/'request.json')
                    prompt=(candidate/'prompt.txt').read_text(encoding='utf-8')
                    wanted=build_messages(cfg,folder,prompt,42+t['call']-1) if key=='h009' else [
                        {'role':'system','content':cfg['system_message']},{'role':'user','content':prompt}]
                    assert request['messages']==wanted
                    assert all('Authorization' not in name for name in request)
                    tokens+=response['prompt_tokens'];outputtokens+=response['generated_tokens']
                selected=read(folder/cfg['arm']/'selected.json')
                program=__import__('pathlib').Path(selected['directory'])/'program.py'
                export=REPORT/'selected_programs';export.mkdir(exist_ok=True)
                shutil.copyfile(program,export/f'fold_{fold}_{key}.py')
                write(export/f'fold_{fold}_{key}_provenance.json',{'selected_call':selected['call'],
                      'program_sha256':sha(program),'run_config':cfg,
                      'features':read(program.parent/'feature_schema.json')['features']})
                apirows.append({'fold':fold,'method':key,'accepted':20,'responses':len(trials),
                                'numeric_distinct_sets':diversity['numeric_distinct_sets'],
                                'selected_call':selected['call'],'selected_constant_control':selected['call'] is None,
                                'input_tokens':tokens,'output_tokens':outputtokens,
                                'actual_POST':len(list((folder/'api_attempts').glob('attempt_*'))),'messages_verified':True})
        arrays.append(np.stack(foldap,axis=1))
    ap=np.concatenate(arrays);foldids=np.asarray(foldids);identities=np.asarray(identities)
    assert ap.shape==(5519,9)
    table=pd.DataFrame(rows);table.to_csv(REPORT/'fold_metrics.csv',index=False)
    pd.DataFrame(apirows).to_csv(REPORT/'api_usage.csv',index=False)
    pd.DataFrame(costs).to_csv(REPORT/'costs.csv',index=False)
    unique,inverse=np.unique(identities,return_inverse=True);counts=np.bincount(inverse)
    sums=np.zeros((len(unique),9));np.add.at(sums,inverse,ap)
    rng=np.random.default_rng(42);bootstrap=[];signs=[]
    for _ in range(50):
        sampled=rng.integers(len(unique),size=(100,len(unique)))
        bootstrap.append(sums[sampled].sum(1)/counts[sampled].sum(1)[:,None])
        signs.append(rng.choice([-1.,1.],size=(100,len(unique)))@sums/len(ap))
    bootstrap=np.concatenate(bootstrap);signs=np.concatenate(signs)
    labels=[v[0] for v in METHODS.values()];keys=list(METHODS)
    summary=[]
    for i,key in enumerate(keys):
        lo,hi=np.quantile(bootstrap[:,i],[.025,.975]);foldscores=table[table.method==key].sort_values('fold')['map'].to_numpy()
        summary.append({'method':key,'label':labels[i],'pooled_map':float(ap[:,i].mean()),'ci95_low':float(lo),'ci95_high':float(hi),
                        'equal_fold_map':float(foldscores.mean()),'fold_maps':foldscores.tolist(),
                        'conditional_catalog_map':float(np.average(table[table.method==key].conditional_catalog_map,
                                                                  weights=table[table.method==key].conditional_users))})
    pairs=[]
    for a,b in itertools.combinations(range(9),2):
        diff=ap[:,a].mean()-ap[:,b].mean();lo,hi=np.quantile(bootstrap[:,a]-bootstrap[:,b],[.025,.975])
        p=(np.sum(np.abs(signs[:,a]-signs[:,b])>=abs(diff))+1)/(len(signs)+1)
        fold_diff=[float(ap[foldids==f,a].mean()-ap[foldids==f,b].mean()) for f in range(3)]
        pairs.append({'a':keys[a],'b':keys[b],'difference':float(diff),'ci95_low':float(lo),'ci95_high':float(hi),
                      'fold_differences':fold_diff,'user_cluster_signflip_p_exploratory':float(p)})
    order=sorted(range(len(pairs)),key=lambda i:pairs[i]['user_cluster_signflip_p_exploratory'])
    previous=0
    for rank,i in enumerate(order):
        previous=max(previous,min(1,(len(pairs)-rank)*pairs[i]['user_cluster_signflip_p_exploratory']))
        pairs[i]['holm_adjusted_p_exploratory']=previous
    result={'status':'passed','rows':len(ap),'unique_customers':len(unique),'folds':3,'model_seed':42,
            'primary':'original-target unconditional MAP@12','summary':summary,'paired_comparisons':pairs,'bootstrap_replicates':len(bootstrap),
            'bootstrap_unit':'original customer; preserve same customer across folds','limitation':'Only3 time blocks and1 model seed; uncertainty conditions on observed weeks/training runs.'}
    write(REPORT/'comparison.json',result)
    pd.DataFrame(summary).to_csv(REPORT/'summary.csv',index=False)
    pd.DataFrame(pairs).to_csv(REPORT/'paired_differences.csv',index=False)
    # Primary comparison: intervals are user-cluster uncertainty, not time/seed uncertainty.
    rank=np.argsort(ap.mean(0));fig,ax=plt.subplots(figsize=(11,6))
    means=ap.mean(0)[rank]*100;ci=np.quantile(bootstrap,[.025,.975],axis=0)[:,rank]*100
    ax.barh(np.arange(9),means,color='#4c78a8',alpha=.8)
    ax.errorbar(means,np.arange(9),xerr=np.maximum(0,np.stack([means-ci[0],ci[1]-means])),fmt='none',ecolor='black',capsize=3)
    ax.set(yticks=np.arange(9),yticklabels=[labels[i] for i in rank],xlabel='Full-target MAP@12 (%)',title='3 temporal folds: paired customer-cluster95% intervals')
    fig.tight_layout();fig.savefig(REPORT/'comparison.png',dpi=170);fig.savefig(REPORT/'comparison.svg');plt.close(fig)
    fig,ax=plt.subplots(figsize=(11,6))
    for i,key in enumerate(keys):
        values=table[table.method==key].sort_values('fold')['map'].to_numpy()*100
        ax.plot(range(3),values,marker='o',label=labels[i])
    ax.set(xticks=range(3),xticklabels=['Aug17','Aug31','Sep14'],ylabel='Full-target MAP@12 (%)',title='Temporal stability; checkpoint selection excludes these weeks')
    ax.legend(fontsize=8,ncol=2);fig.tight_layout();fig.savefig(REPORT/'fold_comparison.png',dpi=170);plt.close(fig)
    fig,axes=plt.subplots(3,3,figsize=(12,9),sharex=True)
    for i,ax in enumerate(axes.flat):
        ax.hist(ap[:,i],bins=np.linspace(0,1,21),color='#4c78a8');ax.set_yscale('log')
        ax.set(title=labels[i],xlabel='Per-user AP@12',ylabel='Count (log)')
    fig.tight_layout();fig.savefig(REPORT/'ap_histograms.png',dpi=150);plt.close(fig)
    diffs=100*(ap.mean(0)[:,None]-ap.mean(0)[None,:]);fig,ax=plt.subplots(figsize=(12,10))
    image=ax.imshow(diffs,cmap='RdBu',vmin=-max(abs(diffs).max(),1e-9),vmax=max(abs(diffs).max(),1e-9))
    ax.set(xticks=range(9),xticklabels=labels,yticks=range(9),yticklabels=labels,title='Row minus column: MAP difference (percentage points)')
    plt.setp(ax.get_xticklabels(),rotation=60,ha='right')
    for i in range(9):
        for j in range(9):ax.text(j,i,f'{diffs[i,j]:+.2f}',ha='center',va='center',fontsize=8)
    fig.colorbar(image,ax=ax);fig.tight_layout();fig.savefig(REPORT/'paired_heatmap.png',dpi=160);plt.close(fig)
    lines=['# Nine methods on larger H&M: temporal cross-validation','',
           '20000 customers,10000 eligible items,5519 outer user-times across3 weeks; one model seed42.',
           'All original positives/users remain in primary MAP, including purchases outside the eligible catalog.',
           'All selections finished before outer scoring. Every trained model was reloaded and checked; API message histories audited.',
           '', '| Method | Fold0 MAP,% | Fold1 | Fold2 | Equal-fold mean | Pooled MAP,% | Customer95% CI | Catalog-conditional MAP,% |',
           '|---|---:|---:|---:|---:|---:|---|---:|']
    for s in sorted(summary,key=lambda s:-s['pooled_map']):
        f=s['fold_maps'];lines.append(f"|{s['label']}|{f[0]*100:.4f}|{f[1]*100:.4f}|{f[2]*100:.4f}|{s['equal_fold_map']*100:.4f}|{s['pooled_map']*100:.4f}|[{s['ci95_low']*100:.4f},{s['ci95_high']*100:.4f}]|{s['conditional_catalog_map']*100:.4f}|")
    lines+=['','![Comparison](comparison.png)','![Per fold](fold_comparison.png)','![Histograms](ap_histograms.png)','![Paired differences](paired_heatmap.png)','',
            'Intervals resample original customers jointly across folds. They do not quantify training-seed variability or performance on unseen time regimes.',
            'All36 pair differences, individual-fold differences and exploratory Holm-adjusted sign-flip p-values are in paired_differences.csv.',
            'A positive average alone is insufficient to label an idea good. Assess magnitude, consistency across3 folds, intervals, runtime and API cost together.',
            'Tests were inspected in earlier project iterations, although these customers were excluded from the old small cohort; this is internal comparison, not a fresh external benchmark.',
            'Requested API model name is gpt-6.1-sol; provider implementation/identity cannot be independently attested.',
            'All six selected API programs and their configuration/provenance are retained in selected_programs/. Constant-control selections, if any, are flagged in api_usage.csv.',
            'costs.csv records native training/search timers. Setup boundaries differ; zero-shot external pretraining and item encoding are excluded. This is not a standardized speed benchmark.',
            '', '[Protocol](../../CVBenchmark/PROTOCOL.md) · [Fold metrics](fold_metrics.csv) · [API usage](api_usage.csv)']
    (REPORT/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(pd.DataFrame(summary)[['label','pooled_map','equal_fold_map']].to_string(index=False),flush=True)

if __name__=='__main__':main()
