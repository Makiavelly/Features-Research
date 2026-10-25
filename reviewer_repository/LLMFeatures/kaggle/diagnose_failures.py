"""Read-only rejection audit. In Kaggle run diagnose(OUT) after stopping the search cell."""
from collections import Counter
import json
from pathlib import Path


def diagnose(out,last=5):
    out=Path(out)
    trials=[]
    for directory in sorted((out/'candidates').glob('candidate_*')):
        trial_file=directory/'trial.json'
        if not trial_file.exists():
            continue
        trial=json.loads(trial_file.read_text())
        response_file=directory/'response.json'
        response=json.loads(response_file.read_text()) if response_file.exists() else {}
        trials.append((directory,trial,response))
    print('Completed calls:',len(trials))
    print('Statuses:',dict(Counter(t.get('status') for _,t,_ in trials)))
    print('Truncated responses:',sum(bool(r.get('truncated')) for _,_,r in trials))
    print('Most common errors (last nonempty traceback line):')
    errors=Counter()
    for _,t,_ in trials:
        if t.get('status')!='valid':
            lines=[s.strip() for s in t.get('error','').splitlines() if s.strip()]
            errors[lines[-1] if lines else '(no error text)']+=1
    for message,count in errors.most_common(10):
        print(count,':',message)
    for directory,trial,response in trials[-last:]:
        print('\n===',directory.name,'island',trial.get('island'),'repair',trial.get('repair'),'===')
        print('status:',trial.get('status'),'tokens:',response.get('generated_tokens'),
              'truncated:',response.get('truncated'),'LLM seconds:',response.get('seconds'))
        print('ERROR:\n'+trial.get('error','(none)'))
        for name in ['schema.json','model.txt','search_metrics.json']:
            print(name,':',(directory/name).exists())
    return {'completed_calls':len(trials),'error_counts':dict(errors)}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('out',type=Path)
    parser.add_argument('--last',type=int,default=5)
    args=parser.parse_args()
    diagnose(args.out,args.last)
