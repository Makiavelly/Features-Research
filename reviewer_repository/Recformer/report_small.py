"""Compare verified Recformer variants with frozen small-pilot predictions."""
from pathlib import Path
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
BASE=ROOT/'Recformer/results/hm_small_seed42_v1'
OUT=ROOT/'reports/recformer_small_v1'
OUT.mkdir(parents=True,exist_ok=True)
verification=json.loads((BASE/'verification.json').read_text())
assert verification['passed']
task=load_dataset(ROOT/'data/rel-hm-small-v1').load_task('user-item-purchase')
rows=pd.read_csv(ROOT/'reports/contextgnn_small_v1/comparison.csv').to_dict('records')
aps={}
def ap_per_user(pred,targets):
    result=[]
    for p,true in zip(pred,targets):
        hit=np.isin(p,true)
        result.append((np.cumsum(hit)/np.arange(1,13)*hit).sum()/min(12,len(true)))
    return np.array(result)
for kind in ['zero_shot','finetuned']:
    folder=BASE/kind
    result=json.loads((folder/'metrics.json').read_text())
    row={'method':'Recformer '+kind,'training_seconds':result['training_and_validation_seconds']}
    for split in ['val','test']:
        pred=np.load(folder/f'{split}_predictions.npy')
        targets=task.get_table(split,mask_input_cols=False).df.article_id
        assert pred.shape==(len(targets),12)
        assert np.all(np.diff(np.sort(pred,axis=1),axis=1)>0)
        assert np.all((pred>=0)&(pred<5000))
        ap=ap_per_user(pred,targets)
        assert abs(ap.mean()-result[split+'_metrics']['map'])<1e-12
        row[('validation' if split=='val' else 'test')+'_map_percent']=100*ap.mean()
        row[split+'_inference_seconds']=result[split+'_inference_seconds']
        if split=='test': aps[kind]=ap
    rows.append(row)
    record('recformer_complete','Recformer '+kind+': complete and independently verified',
           'hm_recformer_small_seed42_v1_'+kind,status='complete',
           val_metrics=result['val_metrics'],test_metrics=result['test_metrics'],artifacts=str(folder.relative_to(ROOT)))
table=pd.DataFrame(rows)
table.to_csv(OUT/'comparison.csv',index=False)
fig,axes=plt.subplots(1,2,figsize=(15,5),sharey=True)
for ax,split in zip(axes,['validation','test']):
    values=table[split+'_map_percent']
    bars=ax.barh(table.method,values,color=['#94a3b8']*6+['#d89d38','#2864b4'])
    ax.bar_label(bars,fmt='%.3f',padding=3)
    ax.set_title(split.capitalize())
    ax.set_xlabel('MAP@12 (%)')
    ax.set_xlim(0,max(values)*1.2)
fig.suptitle('Frozen H&M small-v1: full 5,000-item catalog')
fig.tight_layout()
fig.savefig(OUT/'comparison.png',dpi=150)
plt.close(fig)
history=json.loads((BASE/'history.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(10,4))
x=np.arange(1,len(history)+1)
axes[0].plot(x,[r['train_loss'] for r in history],marker='o')
axes[0].set_ylabel('Weekly multi-positive loss')
axes[1].plot(x,[100*r['val_metrics']['map'] for r in history],marker='o')
axes[1].set_ylabel('Validation MAP@12 (%)')
for ax in axes:
    ax.set_xlabel('Epoch (1-2: stage 1; 3-4: stage 2)')
    ax.set_xticks(x)
fig.tight_layout()
fig.savefig(OUT/'learning_curves.png',dpi=150)
plt.close(fig)
bootstrap={}
refs={'zero_shot':aps['zero_shot']}
for kind in ['contextgnn','idgnn','lightgbm_manual','lightgbm_idgnn','two_tower']:
    pred=np.load(ROOT/'ContextGNN/results/hm_small_v1'/kind/'test_predictions.npy')
    refs[kind]=ap_per_user(pred,task.get_table('test',mask_input_cols=False).df.article_id)
for kind,ap in refs.items():
    delta=aps['finetuned']-ap
    rng=np.random.default_rng(42)
    means=delta[rng.integers(0,len(delta),size=(10000,len(delta)))].mean(axis=1)*100
    bootstrap[kind]={'delta_percentage_points':float(delta.mean()*100),
                     'paired_user_bootstrap_95ci_pp':np.quantile(means,[.025,.975]).tolist()}
(OUT/'bootstrap.json').write_text(json.dumps(bootstrap,indent=2))
zero_bootstrap={}
for kind,ap in refs.items():
    if kind=='zero_shot': continue
    delta=aps['zero_shot']-ap
    rng=np.random.default_rng(42)
    means=delta[rng.integers(0,len(delta),size=(10000,len(delta)))].mean(axis=1)*100
    zero_bootstrap[kind]={'delta_percentage_points':float(delta.mean()*100),
                          'paired_user_bootstrap_95ci_pp':np.quantile(means,[.025,.975]).tolist()}
(OUT/'zero_shot_bootstrap.json').write_text(json.dumps(zero_bootstrap,indent=2))
text=['# Recformer на малом H&M','',
      'Результаты проверены повторным полным инференсом из checkpoint и сохранённого item cache.',
      'Данные: неизменный small-v1; train4804, val304, test250; каталог5000; MAP@12.',
      'Выбор только по validation. Zero-shot и дообученный варианты оценены на test после фиксации модели.','',
      '| Модель | Validation MAP, % | Test MAP, % |','|---|---:|---:|']
for row in rows:
    text.append(f"| {row['method']} | {row['validation_map_percent']:.5f} | {row['test_map_percent']:.5f} |")
text += ['', '![Сравнение](comparison.png)','![Кривые обучения](learning_curves.png)','',
         'Реализация: репликация AaronHeee/RecFormer commit26b00a58e7affe0c54a89c143ea7bce37f2e8e08.',
         'Предобученные веса получены по ссылке репликации; их источник не назван проверенным авторским checkpoint.',
         'Изменения: недельный многопозитивный fullsoftmax,256tokens,FP16,batch4,accum4,2+2эпохи,seed42.',
         'Представления товаров обновляются в стадии1 и фиксированы в стадии2; сохраняются вместе с моделью.',
         'Один seed и250test пользователей дают предварительную оценку. Внешнее предобучение отличается от GNN baseline.',
         'Все10файлов subset проверены по прежним SHA256: subset_integrity.json. Состав и разбиения не менялись.',
         'При выбранном текстовом представлении5000товаров дают4846уникальных токенизированных описаний. У модели нет содержательного признака для различения товаров с одинаковым входом; tie-break поID не добавляет предиктивной информации.',
         'Метрики малого набора не сравнивать напрямую с полным H&M или статьёй.',
         'Bootstrap интервалы являются описательным сравнением замороженных моделей, без выбора параметров по test.',
         'Точные времена и GPU память: Recformer/results/hm_small_seed42_v1/{zero_shot,finetuned}/metrics.json.',
         'Подготовка и smoke замер отделены от обучения; zero-shot training_seconds=0 не включает предобучение и кодирование каталога.','']
selected=json.loads((BASE/'finetuned/metrics.json').read_text())
text += [f"Выбранный дообученный checkpoint: стадия {selected['selected_stage']}, эпоха {selected['selected_epoch']}.",
         f"Обучение и validation: {selected['training_and_validation_seconds']/60:.2f} мин. Пик выделенной CUDA памяти: {selected['peak_cuda_bytes']/2**30:.2f} GiB.",
         '', '| Сравнение дообученного Recformer | Разница test MAP, п.п. | Парный bootstrap 95%, п.п. |',
         '|---|---:|---:|']
for name,b in bootstrap.items():
    lo,hi=b['paired_user_bootstrap_95ci_pp']
    text.append(f"| против {name} | {b['delta_percentage_points']:+.4f} | [{lo:+.4f}; {hi:+.4f}] |")
text.append('')
text += ['| Сравнение zero-shot Recformer | Разница test MAP, п.п. | Парный bootstrap 95%, п.п. |',
         '|---|---:|---:|']
for name,b in zero_bootstrap.items():
    lo,hi=b['paired_user_bootstrap_95ci_pp']
    text.append(f"| против {name} | {b['delta_percentage_points']:+.4f} | [{lo:+.4f}; {hi:+.4f}] |")
text += ['', 'Эти интервалы описывают сравнение уже зафиксированных моделей; дополнительные настройки и запуски по test не выбирались.', '']
(OUT/'report.md').write_text('\n'.join(text),encoding='utf-8')
record('recformer_report','Recformer small report generated after full independent replay; old reports unchanged',
       'hm_recformer_small_seed42_v1',status='complete',artifacts=str(OUT.relative_to(ROOT)),comparison=rows,bootstrap=bootstrap,zero_shot_bootstrap=zero_bootstrap)
print(table.to_string(index=False))
