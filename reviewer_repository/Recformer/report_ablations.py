"""Verified comparisons of two fixed-budget Recformer ablations."""
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
OUT=ROOT/'reports/recformer_ablations_v1'
OUT.mkdir(parents=True,exist_ok=True)
OLD=ROOT/'Recformer/results/hm_small_seed42_v1'
VARIANTS=['low_lr_warmup','freeze_lower6']
LABELS={'low_lr_warmup':'Recformer LR1e-5 + warmup/decay',
        'freeze_lower6':'Recformer frozen embeddings + lower6'}

def dump(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def ap(pred,targets):
    values=[]
    assert pred.shape==(len(targets),12)
    assert np.all((pred>=0)&(pred<5000))
    assert np.all(np.diff(np.sort(pred,axis=1),axis=1)>0)
    for p,true in zip(pred,targets):
        hit=np.isin(p,true)
        values.append((np.cumsum(hit)/np.arange(1,13)*hit).sum()/min(12,len(true)))
    return np.array(values)

task=load_dataset(ROOT/'data/rel-hm-small-v1').load_task('user-item-purchase')
targets={s:task.get_table(s,mask_input_cols=False).df.article_id for s in ['val','test']}
rows=pd.read_csv(ROOT/'reports/recformer_small_v1/comparison.csv').to_dict('records')
baselines={k:np.load(OLD/k/'test_ap.npy') for k in ['zero_shot','finetuned']}
baselines['contextgnn']=ap(np.load(ROOT/'ContextGNN/results/hm_small_v1/contextgnn/test_predictions.npy'),targets['test'])
checks={}
histories={}
all_results={}
bootstraps={}
diagnostics={}
for variant in VARIANTS:
    base=ROOT/'Recformer/results'/f'hm_small_{variant}_seed42_v1'
    cfg=json.loads((base/'config.json').read_text())
    verification=json.loads((base/'verification.json').read_text())
    frozen=json.loads((base/'frozen_verification.json').read_text())
    assert verification['passed'] and frozen['passed']
    digest=hashlib.sha256((ROOT/'Recformer/run_ablations.py').read_bytes()).hexdigest()
    assert digest==cfg['runner_sha256']
    assert cfg['subset_sha256']==json.loads((OLD/'config.json').read_text())['subset_sha256']
    histories[variant]=json.loads((base/'history.json').read_text())
    assert len(histories[variant])==4 and all(h['rows']==4804 for h in histories[variant])
    checks[variant]={'replay':verification,'frozen_weights':frozen,'runner_hash_matches':True,
                     'full_train_rows_each_epoch':True,'zero_shot_matches_original':{}}
    for split in ['val','test']:
        pred=np.load(base/'zero_shot'/f'{split}_predictions.npy')
        original=np.load(OLD/'zero_shot'/f'{split}_predictions.npy')
        scores=np.load(base/'zero_shot'/f'{split}_scores.npy')
        old_scores=np.load(OLD/'zero_shot'/f'{split}_scores.npy')
        assert np.array_equal(pred,original) and np.array_equal(scores,old_scores)
        checks[variant]['zero_shot_matches_original'][split]=True
    folder=base/'finetuned'
    result=json.loads((folder/'metrics.json').read_text())
    all_results[variant]=result
    row={'method':LABELS[variant],'training_seconds':result['training_and_validation_seconds']}
    diagnostics[variant]={}
    for split in ['val','test']:
        pred=np.load(folder/f'{split}_predictions.npy')
        values=ap(pred,targets[split])
        assert abs(values.mean()-result[split+'_metrics']['map'])<1e-12
        row[('validation' if split=='val' else 'test')+'_map_percent']=100*values.mean()
        row[split+'_inference_seconds']=result[split+'_inference_seconds']
        frequency=np.bincount(pred.ravel(),minlength=5000)
        diagnostics[variant][split]={'unique_top12_items':len(np.unique(pred)),
            'largest_single_item_user_share':float(frequency.max()/len(pred)),
            'fraction_users_with_hit':float(np.mean(values>0))}
        if split=='test':
            bootstraps[variant]={}
            for name,reference in baselines.items():
                delta=values-reference
                rng=np.random.default_rng(42)
                samples=delta[rng.integers(0,len(delta),size=(10000,len(delta)))].mean(1)*100
                bootstraps[variant][name]={'difference_pp':float(delta.mean()*100),
                     'paired_user_bootstrap95_pp':np.quantile(samples,[.025,.975]).tolist()}
    selection=json.loads((base/'selection.json').read_text())
    pretest=json.loads((base/'selection_pretest.json').read_text())
    assert pretest['test_predictions_absent'] and pretest['selected_kind']==selection['selected_kind']
    checks[variant]['selection_pretest']=pretest
    z=json.loads((base/'zero_shot/metrics.json').read_text())
    expected='finetuned' if result['val_metrics']['map']>z['val_metrics']['map'] else 'zero_shot'
    assert selection['selected_kind']==expected
    result['selection']=selection
    rows.append(row)
    record('recformer_ablation_complete',f'Recformer {variant} independently verified; selection byval including epoch0',
           f'hm_recformer_small_{variant}_seed42_v1',status='complete',epoch=4,
           val_metrics=result['val_metrics'],test_metrics=result['test_metrics'],
           selection=selection,training_seconds=result['training_and_validation_seconds'],
           artifacts=str(base.relative_to(ROOT)))
table=pd.DataFrame(rows)
table.to_csv(OUT/'comparison.csv',index=False)
fig,axes=plt.subplots(1,2,figsize=(17,7),sharey=True)
colors=['#94a3b8']*6+['#d89d38','#6484a5','#2969b0','#3d9b71']
for ax,split in zip(axes,['validation','test']):
    values=table[split+'_map_percent']
    bars=ax.barh(table.method,values,color=colors)
    ax.bar_label(bars,fmt='%.3f',padding=3)
    ax.set_title(split.capitalize())
    ax.set_xlabel('MAP@12 (%)')
    ax.set_xlim(0,max(values)*1.2)
fig.suptitle('Frozen H&M small-v1: same 5,000-item catalog; 2+2 training epochs')
fig.tight_layout()
fig.savefig(OUT/'comparison.png',dpi=150)
plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(12,4.8))
old_history=json.loads((OLD/'history.json').read_text())
for key,label,history in [('original','Original full fine-tuning',old_history)]+[(v,LABELS[v],histories[v]) for v in VARIANTS]:
    axes[0].plot(range(1,5),[h['train_loss'] for h in history],marker='o',label=label)
    axes[1].plot(range(1,5),[100*h['val_metrics']['map'] for h in history],marker='o',label=label)
axes[1].axhline(2.6699561403508776,color='#d89d38',linestyle='--',label='Zero-shot validation')
axes[0].set_ylabel('Weekly multi-positive loss')
axes[1].set_ylabel('Validation MAP@12 (%)')
for ax in axes:
    ax.set_xlabel('Epoch (1-2: stage1; 3-4: stage2)')
    ax.set_xticks([1,2,3,4])
    ax.axvline(2.5,color='#999999',linestyle=':',alpha=.6)
    ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(OUT/'learning_curves.png',dpi=150)
plt.close(fig)
updates=np.arange(histories['low_lr_warmup'][-1]['optimizer_updates'])
scale=np.where(updates<100,(updates+1)/100,(1204-updates)/1104)
fig,ax=plt.subplots(figsize=(9,3.8))
ax.plot(updates,1e-5*scale,label='Lower LR + warmup/decay')
ax.axhline(5e-5,color='#3d9b71',label='Original / freeze-lower6: constant LR')
ax.set_xlabel('Successful optimizer update')
ax.set_ylabel('Learning rate')
ax.set_xlim(0,max(histories[v][-1]['optimizer_updates'] for v in VARIANTS)-1)
ax.legend()
fig.tight_layout()
fig.savefig(OUT/'learning_rates.png',dpi=150)
plt.close(fig)
dump('verification.json',{'passed':True,'checks':checks})
dump('bootstrap.json',bootstraps)
dump('diagnostics.json',diagnostics)
dump('results.json',all_results)
text=['# Recformer: learning rate и заморозка нижних слоёв','',
      'Два отдельных запуска от одних предобученных весов. Старые результаты сохранены.',
      'Данные и оценка одинаковы: small-v1,4804train/304val/250test,все5000товаров,MAP@12.',
      'В каждом запуске2+2эпохи,seed42. Сначала оба обучены и выбраны поval,только затем оценены наtest.',
      'График показывает лучшие обученные checkpoints; выбор с допустимой эпохой0 показан отдельно.','',
      '| Модель | Validation MAP, % | Test MAP, % |','|---|---:|---:|']
for row in rows:
    text.append(f"| {row['method']} | {row['validation_map_percent']:.5f} | {row['test_map_percent']:.5f} |")
text+=['','![Сравнение](comparison.png)','![Кривые](learning_curves.png)','![LR](learning_rates.png)','']
for v in VARIANTS:
    result=all_results[v]; cfg=result['config']; selected=result['selection']
    text += [f"## {LABELS[v]}",'',
      f"Лучший обученный checkpoint: стадия{result['selected_stage']},эпоха{result['selected_epoch']}. Обучение+validation:{result['training_and_validation_seconds']/60:.2f}мин.",
      f"Пик выделеннойCUDA памяти:{result['peak_cuda_bytes_training']/2**30:.2f}GiB.",
      f"Параметры:{cfg['parameter_counts']}. РежимLR:{cfg['scheduler']}.",
      f"Успешных обновлений:{histories[v][-1]['optimizer_updates']};пропусковAMP:{histories[v][-1]['amp_skipped_updates']}.",
      f"При разрешённой эпохе0 поvalidation выбран:{selected['selected_kind']}; val/testMAP:{100*selected['val_metrics']['map']:.5f}%/{100*selected['test_metrics']['map']:.5f}%.",'',
      '| Сравнение обученного варианта | Разница test MAP, п.п. | Парный bootstrap95%, п.п. |','|---|---:|---:|']
    for name,b in bootstraps[v].items():
        lo,hi=b['paired_user_bootstrap95_pp']
        text.append(f"| против {name} | {b['difference_pp']:+.4f} | [{lo:+.4f}; {hi:+.4f}] |")
    text.append('')
text += ['LR1e-5 иwarmup/decay изменены совместно: отдельно их эффекты не разделены.',
         'Заморозка проверена отдельно при прежнемconstantLR5e-5; embeddings+нижние6из12слоёв не менялись поSHA.',
         'Полные scores/top12 обоих вариантов повторены в независимых процессах. Zero-shot точно совпал с прежним контролем.',
         'Одинseed и250test пользователей ограничивают выводы; bootstrap описывает фиксированные модели,а не вариативность обучения.',
         'Настройки поtest не выбирались; большее число эпох требует отдельного протокола. Это адаптация Recformer к недельным целям H&M,не воспроизведение метрик статьи.','']
(OUT/'report.md').write_text('\n'.join(text),encoding='utf-8')
record('recformer_ablations_report','Both Recformer ablations complete with independent replay; new comparison report generated',
       'hm_recformer_ablations_v1',status='complete',artifacts=str(OUT.relative_to(ROOT)),comparison=rows,results=all_results)
print(table.to_string(index=False))
