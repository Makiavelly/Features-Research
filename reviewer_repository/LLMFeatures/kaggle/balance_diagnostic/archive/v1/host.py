"""Small frozen-prompt diagnostic, not an evolutionary reproduction."""
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder


def write_json(path,value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def initial_source(root):
    spec=(Path(root)/'specs/specification_balance-scale.txt').read_text()
    return spec.split('@equation.evolve\n',1)[1]


def build_prompt(root):
    root=Path(root);spec=(root/'specs/specification_balance-scale.txt').read_text()
    template=ast.literal_eval(ast.parse(spec).body[0].value)
    frame=pd.read_csv(root/'data/balance-scale.csv')
    y=LabelEncoder().fit_transform(frame.iloc[:,-1])
    rows,_=next(StratifiedKFold(n_splits=5,shuffle=True,random_state=42).split(frame.iloc[:,:-1],y))
    train=frame.iloc[rows].reset_index(drop=True)
    descriptions='\n'.join('- '+column+': numerical variable within range [1, 5]' for column in train.columns[:-1])
    examples=[]
    for i in train.sample(10,random_state=42).index:
        parts=[column+' is '+str(train.loc[i,column]) for column in train.columns[:-1]]
        examples.append('If '+', '.join(parts)+', Then Result is '+str(y[rows[i]])+'.')
    for key,value in {'PREFIX':(root/'prompts/domain_head.txt').read_text(),
                      'SUFFIX':(root/'prompts/domain_tail.txt').read_text(),
                      'FEATURES':descriptions,'EXAMPLES':'\n'.join(examples)}.items():
        template=template.replace('['+key+']',value)
    seed=initial_source(root).replace('def modify_features(', 'def modify_features_v0(')
    header='def modify_features_v1(df_input) -> pd.DataFrame:\n    """Improved version of `modify_features_v0`. Think and suggest new features."""\n'
    instruction=('You are a helpful assistant tasked with discovering new features/ dropping less important feaures '
                 'for the given prediction task. Complete the modify_features function below, '
                 'considering the physical meaning and relationships of inputs.\n\n')
    return instruction+template+'\n'+seed+'\n'+header


def evaluate(root,directory):
    directory=Path(directory)
    if (directory/'result.json').exists():return json.loads((directory/'result.json').read_text())
    environment={k:v for k,v in os.environ.items() if not any(t in k.upper() for t in ['TOKEN','SECRET','API_KEY'])}
    environment.update(CUDA_VISIBLE_DEVICES='',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
    command=[sys.executable,str(Path(__file__).with_name('worker.py')),'--data',str(Path(root)/'data/balance-scale.csv'),'--directory',str(directory)]
    try:
        with (directory/'worker.log').open('w') as log:
            completed=subprocess.run(command,env=environment,stdout=log,stderr=subprocess.STDOUT,timeout=90)
        if completed.returncode or not (directory/'result.json').exists():
            raise RuntimeError((directory/'worker.log').read_text()[-3000:])
        return json.loads((directory/'result.json').read_text())
    except Exception as error:
        result={'status':'rejected','phase':'worker','error':str(error)}
        write_json(directory/'result.json',result)
        return result


def controls(root,out):
    results={}
    for name,source in {'raw':'def modify_features(df_input):\n    return df_input.copy()\n',
                        'authors_seed':initial_source(root)}.items():
        directory=Path(out)/name;directory.mkdir(exist_ok=True)
        (directory/'response.txt').write_text(source)
        result=evaluate(root,directory)
        if result['status']!='valid':raise RuntimeError(result)
        results[name]=result
        print(name,'train CV accuracy:',result['cv_accuracy'],flush=True)
    write_json(Path(out)/'controls.json',results)
    return results


def run_diagnostic(root,out,config,generate):
    out=Path(out);prompt=build_prompt(root)
    (out/'prompt_base.txt').write_text(prompt)
    trials=[]
    for mode in config['formats']:
        for seed in config['seeds']:
            directory=out/f'{mode}_seed{seed}';directory.mkdir(exist_ok=True)
            (directory/'prompt.txt').write_text(prompt)
            if (directory/'trial.json').exists():
                trials.append(json.loads((directory/'trial.json').read_text()));continue
            trial={'format':mode,'seed':seed,'directory':str(directory)}
            try:
                response_path=directory/'response.json'
                if response_path.exists():response=json.loads(response_path.read_text())
                else:
                    if (directory/'request.json').exists():raise RuntimeError('Interrupted request consumes diagnostic slot; not silently regenerated')
                    write_json(directory/'request.json',trial)
                    print('LLM call',len(trials)+1,'/6:',mode,'seed',seed,flush=True)
                    response=generate(prompt,seed,mode)
                    write_json(response_path,response)
                trial.update({k:v for k,v in response.items() if k not in {'text','rendered_prompt'}})
                (directory/'response.txt').write_text(response['text'])
                (directory/'rendered_prompt.txt').write_text(response.get('rendered_prompt',prompt))
                if response.get('truncated'):raise ValueError('Truncated at output token limit')
                trial.update(evaluate(root,directory))
            except Exception as error:trial.update(status='rejected',error=str(error))
            write_json(directory/'trial.json',trial)
            trials.append(trial);write_json(out/'trials.json',trials)
            print(mode,seed,trial['status'],'CV:',trial.get('cv_accuracy'),'error:',trial.get('error',''),flush=True)
    return trials


def report(out,config,trials,control_results):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    out=Path(out);summary=[]
    for mode in config['formats']:
        subset=[t for t in trials if t['format']==mode]
        summary.append({'format':mode,'calls':len(subset),'valid':sum(t['status']=='valid' for t in subset),
                        'changed_features':sum(t.get('has_feature_change',False) for t in subset),
                        'truncated':sum(t.get('truncated',False) for t in subset)})
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    axes[0].bar([s['format'] for s in summary],[s['valid'] for s in summary]);axes[0].set(ylabel='Executable /3 calls',ylim=(0,3))
    for mode in config['formats']:
        values=[t['cv_accuracy'] for t in trials if t['format']==mode and t['status']=='valid']
        if values:axes[1].scatter([mode]*len(values),values,label=mode)
    for name,color in [('raw','gray'),('authors_seed','green')]:
        axes[1].axhline(control_results[name]['cv_accuracy'],label=name,color=color)
    axes[1].set_ylabel('Train-only4-fold CV accuracy');axes[1].legend()
    fig.suptitle('Balance-scale diagnostic — NOT paper reproduction / NOT H&M');fig.tight_layout()
    fig.savefig(out/'diagnostic.png',dpi=150);plt.close(fig)
    write_json(out/'summary.json',{'diagnostic_only':True,'paper_reproduction':False,'formats':summary,
        'heldout_evaluated':False,'h_and_m_evaluated':False,'controls':control_results})
    lines=['# Balance-scale Llama diagnostic','',pd.DataFrame(summary).to_string(index=False),'',
           'No H&M or heldout result. Executable output alone does not establish useful feature discovery.',
           'Chat/completion differences suggest format sensitivity;3 draws do not establish causality.',
           'If both fail, inspect responses and model configuration before more H&M search.']
    (out/'report.md').write_text('\n'.join(lines))
    pd.DataFrame([{k:t.get(k) for k in ['format','seed','status','cv_accuracy','has_feature_change','error']} for t in trials]).to_csv(out/'trials.csv',index=False)
    return summary
