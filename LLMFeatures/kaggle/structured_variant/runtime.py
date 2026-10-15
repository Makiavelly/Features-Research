"""Notebook host: paper-style islands, local generation callback and CPU evaluator."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import zipfile
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from worker import RAW, check_program, Data, map_at_12
from structured_features import validate_program, to_sql


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path,obj):
    path=Path(path)
    temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    temp.replace(path)


def locate_bundle(input_root,working,expected_manifest_sha):
    input_root=Path(input_root)
    matches=[]
    for path in input_root.rglob('manifest.json'):
        try:
            if json.loads(path.read_text()).get('bundle_id')=='hm_llmfe_kaggle_fulltrain_v2':
                matches.append(path.parent)
        except (ValueError,OSError):
            pass
    if not matches:
        archives=list(input_root.rglob('hm_llmfe_kaggle_fulltrain_v2.zip'))
        if len(archives)!=1:
            raise FileNotFoundError('Add the supplied hm_llmfe_kaggle_fulltrain_v2.zip as a Kaggle Dataset/Input')
        destination=Path(working)/'hm_llmfe_input'
        destination.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(archives[0]) as z:
            for member in z.infolist():
                if not (destination/member.filename).resolve().is_relative_to(destination.resolve()):
                    raise ValueError('Archive path outside destination')
            z.extractall(destination)
        matches=[destination]
    if len(matches)!=1:
        raise ValueError('Several H&M bundles attached; keep exactly one')
    root=matches[0]
    if sha(root/'manifest.json')!=expected_manifest_sha:
        raise ValueError('Unexpected bundle manifest/version')
    manifest=json.loads((root/'manifest.json').read_text())
    for name,info in manifest['files'].items():
        if sha(root/name)!=info['sha256']:
            raise ValueError('Data checksum mismatch: '+name)
    return root,manifest


def evaluate(data,directory,stage,config):
    directory=Path(directory)
    backend=config.get('backend',config.get('search_backend','lightgbm'))
    result=directory/f'{stage}_metrics.json'
    if result.exists():
        metrics=json.loads(result.read_text())
        if metrics.get('backend')!=backend:
            raise RuntimeError('Cached result uses another evaluator; start a new run ID')
        if stage=='preflight':
            if metrics['program_sha256']!=sha(directory/'program.py'):
                raise RuntimeError('Cached preflight uses another program')
            return metrics
        model_path=directory/('model.txt' if metrics.get('backend')=='lightgbm' else 'model.json')
        if metrics['program_sha256']!=sha(directory/'program.py') or metrics['model_sha256']!=sha(model_path):
            raise RuntimeError('Cached result does not match model/program')
        return metrics
    command=[sys.executable,str(Path(__file__).with_name('worker.py')),'--data',str(data),
             '--directory',str(directory),'--stage',stage,'--threads',str(1 if stage.startswith('replay_') else config['cpu_threads']),
             '--memory-gb',str(config['evaluation_memory_gb']),'--backend',backend]
    env={k:v for k,v in os.environ.items() if not any(s in k.upper() for s in ['TOKEN','SECRET','API_KEY'])}
    env.update(CUDA_VISIBLE_DEVICES='',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    with (directory/f'{stage}.log').open('w') as log:
        try:
            process=subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=config['evaluation_timeout_seconds'])
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Evaluation exceeded {config['evaluation_timeout_seconds']} seconds") from None
    if process.returncode or not result.exists():
        raise RuntimeError((directory/f'{stage}.log').read_text()[-2000:])
    return json.loads(result.read_text())


def source_from_response(text):
    blocks=re.findall(r'```(?:json)?\s*\n(.*?)```',text,re.S|re.I)
    source=blocks[0] if blocks else text
    return json.dumps(validate_program(json.loads(source)),sort_keys=True,indent=2)+'\n'


def source_key(source):
    return hashlib.sha256(json.dumps(validate_program(json.loads(source)),sort_keys=True).encode()).hexdigest()


def choose_demonstrations(memory,rng):
    clusters={}
    for item in memory:
        clusters.setdefault(item['score'],[]).append(item)
    scores=np.array(list(clusters),dtype=float)
    temperature=.1*(1-(len(memory)%10000)/10000)
    weights=np.exp((scores-scores.max())/temperature)
    weights/=weights.sum()
    count=min(3,len(clusters))
    selected=rng.choice(len(scores),size=count,replace=False,p=weights)
    return [clusters[scores[i]][int(rng.integers(len(clusters[scores[i]])))] for i in selected]


def prompt(data,memory,seed):
    demo=choose_demonstrations(memory,np.random.default_rng(seed))
    prior=[{'search_map_fraction':t['score'],'program':json.loads((Path(t['directory'])/'program.py').read_text())} for t in demo]
    return '''Choose useful features for H&M clothing recommendations. Return ONE JSON object only.
Do NOT write SQL or Python. The host compiles your feature descriptions, handles joins and preserves rows.
Goal: predict purchases in the next7days, maximize validation MAP@12 through LightGBM.
History contains only past180 days before each cutoff, for a fixed customer cohort (not full population).
Interface: {"aggregates":[...],"derived":[...]}. Maximum24 aggregates and12 derived formulas.
Start compact: about3-6 aggregates and1-3 derived formulas; limits remain24/12. Entire JSON <=2048 tokens.
AGGREGATE fields: name, keys, op, column, window. Name: unique f_lowercase.
keys: ["customer_id"], ["article_id"], [one clothing category], or ["customer_id", article/category].
Clothing categories: product_code,product_type_no,graphical_appearance_no,colour_group_code,
perceived_colour_value_id,perceived_colour_master_id,department_no,index_group_no,section_no,garment_group_no.
Allowed op: count,count_distinct,sum,avg,min,max,stddev_pop,median.
count MUST use column="*". count_distinct may use customer_id/article_id/sales_channel_id/clothing category
or price/days_ago/customer_age. All OTHER operations may use ONLY price,days_ago,customer_age.
window: integer1..180 days. Default180. price=normalized transaction price, days_ago=days before cutoff.
History is purchases, not views. Time since MOST RECENT purchase uses min on days_ago, not max.
No raw_* fields inside aggregates. sales_channel_id is not a candidate grouping key.
DERIVED fields: name, expr. Expr is a number, {"ref":"existing_feature"}, or {"op":...,"args":[...]}.
Unary op (one arg): abs,log1p,sqrt,negate. Binary op (two args): add,subtract,multiply,divide,min,max,coalesce.
References: aggregate names, EARLIER derived names and raw static fields ONLY. No unknown/future names.
Raw static fields: raw_u_age,raw_u_fn,raw_u_active,raw_u_club_member_status,raw_u_fashion_news_frequency,
and raw_i_ + one clothing category name listed above. No raw_i_fashion_news_frequency exists.
Constants finite +/-1000000; expression depth<=6, nodes<=64. Divide by0 returns missing.
log1p/sqrt clip negative inputs to0. Missing aggregate groups remain missing; use coalesce if desired.
FORMAT EXAMPLE ONLY (choose your own useful complete set):
{"aggregates":[{"name":"f_example","keys":["customer_id"],"op":"count","column":"*","window":30}],
 "derived":[{"name":"f_example_log","expr":{"op":"log1p","args":[{"ref":"f_example"}]}}]}
The host appends the same15 raw fields; do not copy them as new features without a useful transformation.
All803377 training pairs, LightGBM150 rounds/31 leaves; search fixed256 users/6594 candidates.
Each proposal is a complete set, not a patch. Test is not available during selection.
Previously measured sets in this population (empty aggregates is raw control):
'''+json.dumps(prior,separators=(',',':'))


def budget_summary(trials,config):
    measured=sum(t['status']=='valid' for t in trials)
    return {'llm_calls':len(trials),'repair_calls':sum(t.get('repair',0)>0 for t in trials),
            'new_proposals':len({t['proposal'] for t in trials}),
            'rejected':sum(t['status']=='rejected' for t in trials),
            'duplicates':sum(t['status']=='duplicate' for t in trials),
            'evaluated_distinct':measured,'target':config['target_successful_distinct'],
            'max_llm_calls':config['max_llm_calls'],'max_repairs_per_proposal':config['max_repairs_per_proposal'],
            'target_met':measured>=config['target_successful_distinct'],
            'budget_exhausted':len(trials)>=config['max_llm_calls'],
            'prompt_tokens':sum(t.get('prompt_tokens',0) for t in trials),
            'llm_seconds':sum(t.get('llm_seconds',0) for t in trials),
            'generated_tokens':sum(t.get('generated_tokens',0) for t in trials)}


def progress(out,trials,config):
    out=Path(out)
    write_json(out/'trials.json',trials)
    summary=budget_summary(trials,config)
    write_json(out/'search_state.json',summary)
    valid=[t for t in trials if t['status']=='valid']
    fig,axes=plt.subplots(1,3,figsize=(15,4))
    if valid:
        x=[t['sample'] for t in valid]
        y=100*np.array([t['score'] for t in valid])
        axes[0].scatter(x,y,label='Candidate')
        axes[0].step(x,np.maximum.accumulate(y),where='post',label='Best search')
        axes[0].legend()
        axes[1].plot(np.arange(1,len(valid)+1),np.maximum.accumulate(y),marker='.')
        axes[2].hist(y,bins=min(10,len(valid)))
    axes[0].set(xlabel='LLM call (repairs included)',ylabel='Search MAP@12 (%)')
    axes[1].set(xlabel='Distinct evaluated sets',ylabel='Best search MAP@12 (%)')
    axes[2].set(xlabel='Search MAP@12 (%)',ylabel='Evaluated programs')
    fig.suptitle('Search only: fixed256 users/candidates — not test')
    fig.tight_layout();fig.savefig(out/'search_progress.png',dpi=150);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    labels=['valid','rejected','duplicate']
    axes[0].bar(labels,[sum(t['status']==s for t in trials) for s in labels])
    axes[0].set_ylabel('Generated programs')
    for t in valid:
        p=Path(t['directory'])/'learning_curve.json'
        history=json.loads(p.read_text())['train']['logloss']
        axes[1].plot(np.arange(1,len(history)+1),history,label=str(t['sample']),alpha=.7)
    axes[1].set(xlabel='Boosting round',ylabel='Train binary logloss')
    if valid:
        axes[1].legend(ncol=4,fontsize=7)
    fig.tight_layout();fig.savefig(out/'training_and_rejections.png',dpi=150);plt.close(fig)
    lines=['# Search progress','',
           f"LLM calls: {len(trials)}/{summary['max_llm_calls']}; evaluated distinct: {len(valid)}/{summary['target']}; repair calls: {summary['repair_calls']}.",
           'Search validation only; no final test results yet.','',
           '| Call | Proposal | Island | Repair | Parent call | Status | MAP@12, % |','|---|---:|---:|---:|---:|---|---:|']
    for t in trials:
        value=f"{100*t['score']:.5f}" if t['status']=='valid' else '—'
        lines.append(f"| {t['sample']} | {t['proposal']} | {t['island']} | {t['repair']} | {t.get('parent_call') or '—'} | {t['status']} | {value} |")
    lines+=['','![Search](search_progress.png)','![Training](training_and_rejections.png)']
    (out/'progress.md').write_text('\n'.join(lines),encoding='utf-8')


def repair_prompt(base,parent,error):
    return (base+'\nREPAIR: return the COMPLETE corrected JSON. Fix ALL errors listed below, not just the first.\n'
            +'Previous full response:\n'+parent+'\nErrors:\n'+error[-6500:]
            +'\nNo SQL/Python text. Use only the documented operations and namespaces. '
            +'You may remove invalid features and dependent formulas. Keep the set compact. '
            +'For duplicate rejection choose a different useful complete set.')


def search(data,out,config,generate):
    data,out=Path(data),Path(out)
    out.mkdir(parents=True,exist_ok=True)
    if (out/'selected.json').exists():
        return json.loads((out/'selected.json').read_text())
    control=out/'raw_control';control.mkdir(exist_ok=True)
    (control/'program.py').write_text(RAW)
    baseline=evaluate(data,control,'search',config)
    raw={'directory':str(control),'score':baseline['map']}
    memories=[[raw.copy()] for _ in range(3)]
    trials=[]
    seen=set()
    target=config['target_successful_distinct']
    max_calls=config['max_llm_calls']
    max_repairs=config['max_repairs_per_proposal']
    if target<1 or max_calls<1 or max_repairs<0:
        raise ValueError('Positive successful-set/request budgets and nonnegative repair budget required')
    proposal=0
    repair=0
    parent=None
    while len(seen)<target and len(trials)<max_calls:
        index=len(trials)
        batch=proposal//3
        batchdir=out/f'batch_{batch:02d}';batchdir.mkdir(exist_ok=True)
        if not (batchdir/'meta.json').exists():
            island=int(np.random.default_rng(42+batch).integers(3))
            text=prompt(data,memories[island],42+batch)
            (batchdir/'prompt.txt').write_text(text)
            write_json(batchdir/'meta.json',{'island':island,'new_proposals_per_prompt':3,'seed':42+batch})
        meta=json.loads((batchdir/'meta.json').read_text());island=meta['island']
        directory=out/'candidates'/f'candidate_{index+1:03d}';directory.mkdir(parents=True,exist_ok=True)
        if (directory/'trial.json').exists():
            trial=json.loads((directory/'trial.json').read_text())
        else:
            trial={'sample':index+1,'call':index+1,'proposal':proposal+1,'repair':repair,
                   'parent_call':parent['sample'] if parent is not None else None,
                   'island':island,'batch':batch,'directory':str(directory)}
            tick=time.perf_counter()
            failure_stage='generation'
            try:
                response_path=directory/'response.json'
                text=(batchdir/'prompt.txt').read_text()
                if repair:
                    parent_path=Path(parent['directory'])/'response.json'
                    previous=json.loads(parent_path.read_text()).get('text','') if parent_path.exists() else ''
                    # Keep repair prompts within context: prior code + error + raw example,
                    # rather than appending to three potentially long memory programs.
                    text=repair_prompt(prompt(data,[raw],42+proposal),previous,parent['error'])
                (directory/'prompt.txt').write_text(text)
                if response_path.exists():
                    response=json.loads(response_path.read_text())
                else:
                    request_path=directory/'request.json'
                    if request_path.exists():
                        raise RuntimeError('Previous request was interrupted; its budget slot is consumed. Use a new request for repair.')
                    write_json(request_path,{**trial,'seed':42+index})
                    print(f"LLM call{index+1}/{max_calls}, measured{len(seen)}/{target}, island{island}, repair{repair}/{max_repairs}",flush=True)
                    response=generate(text,42+index)
                    write_json(response_path,response)
                for name in ['prompt_tokens','generated_tokens','seconds']:
                    trial['llm_seconds' if name=='seconds' else name]=response.get(name,0)
                trial['truncated']=bool(response.get('truncated'))
                failure_stage='parse_and_validate'
                if response.get('truncated'):
                    raise ValueError('Program truncated at output token limit')
                code=source_from_response(response['text'])
                (directory/'program.py').write_text(code)
                (directory/'program.json').write_text(code)
                write_json(directory/'compiled_sql.json',to_sql(json.loads(code)))
                key=source_key(code);trial['program_key']=key
                if key in seen:
                    trial.update(status='duplicate',error='Duplicate canonical structured specification')
                else:
                    failure_stage='preflight'
                    print(f"call{index+1}: Structured specification validated; checking small time-safe snapshots (not a measured set)",flush=True)
                    preflight=evaluate(data,directory,'preflight',config)
                    trial['preflight']=preflight
                    failure_stage='feature_train_score'
                    print(f"call{index+1}: preflight passed; starting LightGBM on{config.get('train_pairs','configured')} training pairs",flush=True)
                    metrics=evaluate(data,directory,'search',config)
                    trial.update(status='valid',score=metrics['map'],metrics=metrics)
            except Exception as error:
                trial.update(status='rejected',error=str(error),failure_stage=failure_stage)
            trial['elapsed_seconds']=time.perf_counter()-tick
            write_json(directory/'trial.json',trial)
        trials.append(trial)
        if trial['status']=='valid':
            seen.add(trial['program_key'])
            if trial['score']>max(t['score'] for t in memories[island]):
                memories[island].append(trial)
        write_json(out/'memory.json',memories)
        progress(out,trials,config)
        print(f"call{index+1}/{max_calls}, island{island}, repair{repair}: {trial['status']}; measured={len(seen)}/{target}",flush=True)
        if trial['status']!='valid':
            print(f"REJECTION call{index+1}: stage={trial.get('failure_stage','duplicate')}, "
                  f"generated_tokens={trial.get('generated_tokens')}, truncated={trial.get('truncated')}",flush=True)
            print(trial.get('error','No error text saved'),flush=True)
        else:
            print(f"ACCEPTED call{index+1}: search MAP@12={100*trial['score']:.6f}%",flush=True)
        if trial['status']!='valid' and repair<max_repairs:
            repair+=1
            parent=trial
        else:
            proposal+=1
            repair=0
            parent=None
    write_json(out/'search_complete.json',budget_summary(trials,config))
    # Raw control can win; selecting a harmful LLM program is not forced.
    options=[raw]+[t for t in trials if t['status']=='valid']
    options=sorted(options,key=lambda t:t['score'],reverse=True)[:3]
    confirmations=[]
    for t in options:
        metrics=evaluate(data,Path(t['directory']),'confirm',config)
        confirmations.append({'directory':t['directory'],'score':metrics['map'],'metrics':metrics})
        write_json(out/'confirmation.json',confirmations)
    best=max(confirmations,key=lambda t:t['score'])
    selected={**best,'selection':'512 disjoint validation users; frozen before heldout val/test',
              'selected_raw_control':Path(best['directory'])==control,
              'search_budget':budget_summary(trials,config)}
    write_json(out/'selected.json',selected)
    return selected


def final(data,out,config):
    data,out=Path(data),Path(out)
    selected=json.loads((out/'selected.json').read_text())
    winner_name='Search winner: raw control (NO LLM features)' if selected['selected_raw_control'] else 'LLM-FE LightGBM'
    choices={'Raw LightGBM':out/'raw_control',winner_name:Path(selected['directory'])}
    metrics={}
    for name,directory in choices.items():
        settings={**config,'backend':'lightgbm'}
        metrics[name]={}
        for split in ['val','test']:
            original=evaluate(data,directory,split,settings)
            replay=evaluate(data,directory,'replay_'+split,settings)
            assert original['map']==replay['map'] and replay['passed']
            metrics[name][split]=original
    # Native reference is never included in prompts or model selection.
    references={'Manual features → LightGBM':'manual_lightgbm',
                'GNN → LightGBM':'gnn_lightgbm',
                'ID-GNN (graph training budget)':'idgnn'}
    for name,label in references.items():
        metrics[name]={}
        for split in ['val','test']:
            targets=pd.read_parquet(data/f'{split}_targets.parquet')
            value,_=map_at_12(np.load(data/f'{split}_{label}_reference.npy'),targets.article_id)
            metrics[name][split]={'map':value,'reference':True}
    frame=pd.DataFrame([{'model':name,'val_map':r['val']['map'],'test_map':r['test']['map']} for name,r in metrics.items()])
    frame.to_csv(out/'comparison.csv',index=False)
    fig,ax=plt.subplots(figsize=(10,4))
    for i,split in enumerate(['val','test']):
        bars=ax.barh(np.arange(len(frame))+(i-.5)*.32,100*frame[split+'_map'],height=.32,label=split)
        ax.bar_label(bars,fmt='%.3f',padding=3,fontsize=8)
    ax.set_yticks(np.arange(len(frame)),frame.model);ax.set_xlabel('MAP@12 (%) — identical fixed candidate pools');ax.legend()
    ax.set_xlim(0,max(.1,float(frame[['val_map','test_map']].to_numpy().max())*118))
    if config.get('smoke'):
        fig.suptitle('SYNTHETIC SMOKE — not Llama results')
    fig.tight_layout();fig.savefig(out/'comparison.png',dpi=150,bbox_inches='tight');plt.close(fig)
    aps={name:np.load(path/'test_user_ap.npy') for name,path in choices.items()}
    truth=pd.read_parquet(data/'test_targets.parquet')
    for name,label in references.items():
        aps[name]=map_at_12(np.load(data/f'test_{label}_reference.npy'),truth.article_id)[1]
    pd.DataFrame({'customer_id':truth.customer_id.values,**aps}).to_csv(out/'test_user_ap.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(13,4))
    for name,values in aps.items():
        axes[0].hist(100*values[values>0],bins=np.linspace(0,100,21),histtype='step',label=name)
    axes[0].set(xlabel='Positive user AP@12 (%)',ylabel='Users',yscale='log');axes[0].legend(fontsize=7)
    axes[1].barh(list(aps),[100*np.mean(a==0) for a in aps.values()]);axes[1].set(xlabel='Test users without hits (%)',xlim=(0,100))
    if config.get('smoke'):
        fig.suptitle('SYNTHETIC SMOKE — not Llama results')
    fig.tight_layout();fig.savefig(out/'ap_histograms.png',dpi=150,bbox_inches='tight');plt.close(fig)
    delta=aps[winner_name]-aps['Raw LightGBM']
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    axes[0].bar(['LLM better','Tie','Raw better'],[(delta>0).sum(),(delta==0).sum(),(delta<0).sum()])
    if np.any(delta!=0):
        axes[1].hist(100*delta[delta!=0],bins=30);axes[1].set_yscale('log')
    axes[1].set(xlabel='LLM minus raw AP (percentage points)',ylabel='Users; ties omitted')
    fig.tight_layout();fig.savefig(out/'paired_comparison.png',dpi=150);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for name in ['Raw LightGBM',winner_name]:
        curve=json.loads((choices[name]/'learning_curve.json').read_text())['train']['logloss']
        axes[0].plot(np.arange(1,len(curve)+1),curve,label=name)
    axes[0].set(xlabel='Boosting round',ylabel='Train binary logloss');axes[0].legend()
    delta_lgb=aps[winner_name]-aps['Raw LightGBM']
    axes[1].bar(['LLM better','Tie','Raw better'],[(delta_lgb>0).sum(),(delta_lgb==0).sum(),(delta_lgb<0).sum()])
    axes[1].set_title('LightGBM: paired test AP')
    fig.tight_layout();fig.savefig(out/'lightgbm_comparison.png',dpi=150);plt.close(fig)
    trials=json.loads((out/'trials.json').read_text())
    report={'complete':True,'metrics':metrics,'selected':selected,'config':config,
            'search_budget':budget_summary(trials,config),
            'smoke':bool(config.get('smoke',False)),
            'generated_programs':sum((Path(t['directory'])/'response.json').exists() for t in trials),
            'evaluated_distinct':sum(t['status']=='valid' for t in trials),
            'llm_feature_model_selected':not selected['selected_raw_control'],
            'llm_program_quality_measured':any(t['status']=='valid' for t in trials),
            'independent_full_replay':True,'coverage':'bounded exported subset, not entire H&M',
            'paper_reproduction':False}
    write_json(out/'report.json',report)
    lines=['# Llama3.1-8B → Python features → LightGBM: bounded H&M','',
           'Adaptation of LLM-FE; not a numerical reproduction of the paper. All MAP values in percent.',
           'One seed42,180-day selected-cohort history, frozen shared ID-GNN pools.',
           'LightGBM selects features throughout search and confirmation; all new trees use identical803377 training pairs.',
           'Manual and GNN→LightGBM references use those same803377 supervised pairs and these exact evaluation rows/pools.',
           'Tuning protocols, derived seeds and historical representations differ; GNN also used upstream graph training.',
           'Compare pipeline quality on this subset, not differences in isolated feature quality or full-dataset MAP.',
           'Selection uses only search256 + confirmation512; heldout val1024 and test2048 used after freezing.',
           'Native ID-GNN reference used more training data and is contextual, not a matched-budget comparison.',
           f"LLM calls{len(trials)}/{config['max_llm_calls']}; evaluated distinct{report['evaluated_distinct']}/{config['target_successful_distinct']}; target met: {report['search_budget']['target_met']}. Raw control selected: {selected['selected_raw_control']}.",
           'All raw/LLM heldout predictions reproduced from saved models in separate CPU processes with1 thread.',
           '', '| Model | Validation MAP, % | Test MAP, % |','|---|---:|---:|']
    if config.get('smoke'):
        lines=['# SYNTHETIC SMOKE — not Llama results','',
               'This report tests software using a synthetic generator and tiny data. No real Llama inference or quality experiment.', '']+lines
    if selected['selected_raw_control']:
        lines.insert(2,'RAW CONTROL SELECTED: the search-winner row contains NO LLM features. Do not report its MAP as the quality of LLM-generated features.')
    lines += [f"| {r.model} | {100*r.val_map:.5f} | {100*r.test_map:.5f} |" for r in frame.itertuples()]
    lines += ['',f"Selected program: `{Path(selected['directory']).relative_to(out)}/program.py`.",
              '![MAP](comparison.png)','![AP](ap_histograms.png)','![Paired](paired_comparison.png)',
              '![Search](search_progress.png)','![Training](training_and_rejections.png)',
              '![LightGBM](lightgbm_comparison.png)']
    (out/'report.md').write_text('\n'.join(lines),encoding='utf-8')
    return report
