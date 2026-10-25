"""Matched short-versus-long Recformer comparison after independent replay."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record
from relbench import load_dataset
BASE=ROOT/'Recformer/results/hm_small_long_floor_seed42_v1'
OUT=ROOT/'reports/recformer_long_v1'
OLD=ROOT/'Recformer/results/hm_small_seed42_v1'
OUT.mkdir(parents=True,exist_ok=True)

def dump(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def ap(pred,targets):
    assert pred.shape==(len(targets),12)
    assert np.all((pred>=0)&(pred<5000))
    assert np.all(np.diff(np.sort(pred,axis=1),axis=1)>0)
    values=[]
    for p,true in zip(pred,targets):
        hit=np.isin(p,true)
        values.append((np.cumsum(hit)/np.arange(1,13)*hit).sum()/min(12,len(true)))
    return np.array(values)

verification=json.loads((BASE/'verification.json').read_text())
assert verification['passed']
short_freeze=json.loads((BASE/'short_2plus2/selection_val.json').read_text())
assert short_freeze['checkpoint_sha256']==verification['checks']['short_2plus2']['checkpoint_sha256'],'Short-prefix checkpoint changed after freeze'
cfg=json.loads((BASE/'config.json').read_text())
assert hashlib.sha256((ROOT/'Recformer/run_long.py').read_bytes()).hexdigest()==cfg['runner_sha256']
history=json.loads((BASE/'history.json').read_text())
summary=json.loads((BASE/'training_summary.json').read_text())
pretest=json.loads((BASE/'selection_pretest.json').read_text())
assert pretest['test_predictions_absent']
assert 4<=len(history)<=8 and all(h['rows']==4804 for h in history)
assert len([h for h in history if h['stage']==1])==2
short_best=max(history[:4],key=lambda h:h['val_metrics']['map'])
long_best=max(history,key=lambda h:h['val_metrics']['map'])
assert long_best['val_metrics']['map']>=short_best['val_metrics']['map']
task=load_dataset(ROOT/'data/rel-hm-small-v1').load_task('user-item-purchase')
targets={s:task.get_table(s,mask_input_cols=False).df.article_id for s in ['val','test']}
results={};quality={};diagnostics={}
for kind in ['zero_shot','short_2plus2','finetuned']:
    folder=BASE/kind
    result=json.loads((folder/'metrics.json').read_text())
    results[kind]=result
    quality[kind]={};diagnostics[kind]={}
    for split in ['val','test']:
        pred=np.load(folder/f'{split}_predictions.npy')
        values=ap(pred,targets[split])
        assert abs(values.mean()-result[split+'_metrics']['map'])<1e-12
        quality[kind][split]=values
        frequency=np.bincount(pred.ravel(),minlength=5000)
        diagnostics[kind][split]={'unique_top12_items':len(np.unique(pred)),
              'largest_single_item_user_share':float(frequency.max()/len(pred)),
              'fraction_users_with_hit':float(np.mean(values>0))}
        if kind=='zero_shot':
            assert np.array_equal(pred,np.load(OLD/kind/f'{split}_predictions.npy'))
            assert np.array_equal(np.load(folder/f'{split}_scores.npy'),np.load(OLD/kind/f'{split}_scores.npy'))
    if kind!='zero_shot':
        expected=short_best if kind=='short_2plus2' else long_best
        assert (result['selected_stage'],result['selected_epoch'])==(expected['stage'],expected['epoch'])
for label in ['short','long']:
    assert json.loads((BASE/f'selection_{label}.json').read_text())['selected_kind']==pretest[label]['selected_kind']
rows=pd.read_csv(ROOT/'reports/recformer_ablations_v1/comparison.csv').to_dict('records')
labels={'short_2plus2':'Recformer matched2+2 (LRfloor)', 'finetuned':f'Recformer long ({len(history)}epochs; LRfloor)'}
for kind in ['short_2plus2','finetuned']:
    r=results[kind]
    rows.append({'method':labels[kind],'validation_map_percent':100*r['val_metrics']['map'],
        'test_map_percent':100*r['test_metrics']['map'],'training_seconds':r['training_and_validation_seconds'],
        'val_inference_seconds':r['val_inference_seconds'],'test_inference_seconds':r['test_inference_seconds']})
table=pd.DataFrame(rows)
table.to_csv(OUT/'comparison.csv',index=False)
fig,axes=plt.subplots(1,2,figsize=(18,8),sharey=True)
colors=['#94a3b8']*6+['#d89d38','#6484a5','#537daf','#579e7c','#8d6bb2','#256ab5']
for ax,split in zip(axes,['validation','test']):
    vals=table[split+'_map_percent']
    bars=ax.barh(table.method,vals,color=colors)
    ax.bar_label(bars,fmt='%.3f',padding=3)
    ax.set_xlabel('MAP@12 (%)');ax.set_title(split.capitalize())
    ax.set_xlim(0,max(vals)*1.2)
fig.suptitle('Frozen H&M small-v1: full5,000catalog; matched short/long prefix control')
fig.tight_layout();fig.savefig(OUT/'comparison.png',dpi=150);plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(12,4.8))
x=np.arange(1,len(history)+1)
axes[0].plot(x,[h['train_loss'] for h in history],marker='o',label='Current LRfloor trajectory')
axes[1].plot(x,[100*h['val_metrics']['map'] for h in history],marker='o',label='Per-epoch validation')
axes[1].plot(x,np.maximum.accumulate([100*h['val_metrics']['map'] for h in history]),linestyle=':',label='Best trained checkpoint so far')
axes[1].axhline(2.6699561403508776,color='#d89d38',linestyle='--',label='Zero-shot validation')
axes[0].set_ylabel('Weekly multi-positive loss');axes[1].set_ylabel('Validation MAP@12 (%)')
for ax in axes:
    ax.set_xlabel('Global epoch (stage1=1-2; stage2>=3)');ax.set_xticks(x)
    ax.axvline(2.5,color='#888888',linestyle=':',alpha=.6)
    ax.axvline(4.5,color='#8d6bb2',linestyle='--',alpha=.6,label='End of matched short prefix')
    ax.legend(fontsize=7)
fig.tight_layout();fig.savefig(OUT/'learning_curves.png',dpi=150);plt.close(fig)
updates=np.arange(summary['optimizer_updates'])
scale=np.where(updates<100,(updates+1)/100,np.maximum(.1,.1+.9*(1204-updates)/1104))
fig,ax=plt.subplots(figsize=(9,4))
ax.plot(updates,scale*1e-5,label='Shared short/long LR schedule')
ax.axhline(1e-6,color='#8d6bb2',linestyle='--',label='Nonzero floor1e-6')
ax.axvline(history[3]['optimizer_updates'],color='#888888',linestyle=':',label='Four-epoch prefix ends')
ax.set_xlabel('Successful optimizer update');ax.set_ylabel('Learning rate');ax.legend()
fig.tight_layout();fig.savefig(OUT/'learning_rates.png',dpi=150);plt.close(fig)
references={'matched_short':quality['short_2plus2']['test'],'zero_shot':quality['zero_shot']['test'],
 'previous_LR_warmup':np.load(ROOT/'Recformer/results/hm_small_low_lr_warmup_seed42_v1/finetuned/test_ap.npy'),
 'contextgnn':ap(np.load(ROOT/'ContextGNN/results/hm_small_v1/contextgnn/test_predictions.npy'),targets['test'])}
bootstrap={}
for name,reference in references.items():
    delta=quality['finetuned']['test']-reference
    rng=np.random.default_rng(42)
    samples=delta[rng.integers(0,len(delta),size=(10000,len(delta)))].mean(1)*100
    bootstrap[name]={'difference_pp':float(delta.mean()*100),'paired_user_bootstrap95_pp':np.quantile(samples,[.025,.975]).tolist()}
same_sha=verification['checks']['short_2plus2']['checkpoint_sha256']==verification['checks']['finetuned']['checkpoint_sha256']
dump('bootstrap.json',bootstrap);dump('diagnostics.json',diagnostics)
dump('results.json',{'models':results,'training_summary':summary,'selection_pretest':pretest,'short_long_same_checkpoint':same_sha})
dump('verification.json',{'passed':True,'replay':verification,'runner_hash_matches':True,'zero_shot_matches_original':True,'selection_frozen_before_test':True})
text=['# Recformer: больше эпох и сопоставимый короткий контроль','',
      f"Выполнено {len(history)}полных эпох:2первой стадии и{len(history)-2}второй. Причина остановки:{summary['stop_reason']}.",
      f"Обучение+validation:{summary['training_and_validation_seconds']/60:.2f}мин;короткий префикс:{summary['short_training_and_validation_seconds']/60:.2f}мин.",
      'Это одна траектория обучения с одинаковыми первыми4эпохами,из которой сохранены два правила выбораcheckpoint.',
      'LRwarmup100до1e-5,decayдо1e-6кupdate1204,далееconstant. Прежний4эпохrunсdecayк0показан как отдельный reference,не matchedконтроль.',
      'Малый набор/разбиения/полный5000каталог не менялись;train4804,val304,test250;seed42.',
      'Все решения поvalidation записаны доtest. Epoch0допустимвотдельных selection_short/long.json.',
      'Длинныйbestvalне может быть ниже короткого поопределению:выбирается из большего множества checkpoints.','',
      '| Модель | Validation MAP, % | Test MAP, % |','|---|---:|---:|']
for row in rows:
    text.append(f"| {row['method']} | {row['validation_map_percent']:.5f} | {row['test_map_percent']:.5f} |")
text+=['','![Сравнение](comparison.png)','![Кривые](learning_curves.png)','![LR](learning_rates.png)','',
       f"Короткий checkpoint:stage{short_best['stage']},epoch{short_best['epoch']};длинный:stage{long_best['stage']},epoch{long_best['epoch']}. Совпадают поSHA:{same_sha}.",
       '', '| Длинный минус | Разница test MAP, п.п. | Парный bootstrap95%, п.п. |','|---|---:|---:|']
for name,b in bootstrap.items():
    lo,hi=b['paired_user_bootstrap95_pp']
    text.append(f"| {name} | {b['difference_pp']:+.4f} | [{lo:+.4f}; {hi:+.4f}] |")
text+=['','Все6полных val/testreplayпрошли,включаяполныеscores/top12. Zero-shotсовпалс прежним контролем.',
       'Одинseed и250testпользователей;bootstrapописывает фиксированные модели,а не разброс обучения. Настройкипоtestнеподбирались.',
       'Это адаптация Recformer к недельным H&M целям,не воспроизведение метрик статьи. Старые результаты и окружение сохранены.','']
(OUT/'report.md').write_text('\n'.join(text),encoding='utf-8')
for kind in ['zero_shot','short_2plus2','finetuned']:
    r=results[kind]
    record('recformer_long_model_verified','Long experiment '+kind+': measured and independently verified',
        'hm_recformer_small_long_floor_seed42_v1_'+kind,status='complete',val_metrics=r['val_metrics'],
        test_metrics=r['test_metrics'],artifacts=str((BASE/kind).relative_to(ROOT)))
record('recformer_long_report','Long Recformer experiment complete; matched short/long comparison verified',
       'hm_recformer_small_long_floor_seed42_v1',status='complete',epoch=len(history),
       val_metrics=results['finetuned']['val_metrics'],test_metrics=results['finetuned']['test_metrics'],
       training_summary=summary,bootstrap=bootstrap,artifacts=str(OUT.relative_to(ROOT)))
print(table.to_string(index=False))
