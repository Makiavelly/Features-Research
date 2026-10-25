"""Tables and plots separating repetition, discovery and catalog coverage."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import novelty_audit as audit
from common import read,write,sha,record,ROOT


def main():
    dest=audit.REP
    table=pd.read_csv(dest/'metrics.csv')
    users=pd.read_parquet(dest/'per_user_metrics.parquet')
    coverage=read(dest/'coverage.json')
    principal=[]
    for mode in ['normal','new_only']:
        part=users[(users['mode']==mode)&(users['group']=='new')]
        for other in ['contextgnn_old','idgnn','recformer_zero','recformer_tuned','manual','h008_20','h009_40']:
            a=part[part.method=='contextgnn'].sort_values(['fold','row'])
            b=part[part.method==other].sort_values(['fold','row'])
            assert np.array_equal(a[['fold','row']],b[['fold','row']])
            for metric in ['available_recall','map']:
                eligible=a[metric].notna().to_numpy()
                assert np.array_equal(eligible,b[metric].notna())
                delta=a[metric].to_numpy()[eligible]-b[metric].to_numpy()[eligible]
                customers=a.customer.to_numpy()[eligible]
                unique,inverse=np.unique(customers,return_inverse=True)
                counts=np.bincount(inverse);sums=np.bincount(inverse,weights=delta)
                rng=np.random.default_rng(42);boot=[]
                for _ in range(5000):
                    ix=rng.integers(0,len(unique),size=len(unique))
                    boot.append(sums[ix].sum()/counts[ix].sum())
                low,high=np.quantile(boot,[.025,.975])
                principal.append(dict(mode=mode,group='new',metric=metric,a='contextgnn',b=other,
                    delta=float(delta.mean()),ci95_low=float(low),ci95_high=float(high),observations=len(delta)))
    pd.DataFrame(principal).to_csv(dest/'paired_novelty_contrasts.csv',index=False)
    normal=table[(table['mode']=='normal')&(table['group']=='all')].sort_values('map')
    keys=normal.method.tolist();labels=normal.label.tolist()
    colors=['#4c78a8','#f58518','#54a24b','#e45756','#999999']
    fig,ax=plt.subplots(figsize=(14,10))
    left=np.zeros(len(keys))
    for group,color in zip(audit.GROUPS,colors):
        values=np.array([table[(table.method==key)&(table['mode']=='normal')&(table['group']==group)].ap_contribution.iloc[0] for key in keys])*100
        ax.barh(range(len(keys)),values,left=left,color=color,label=audit.LABELS[group]);left+=values
    ax.set(yticks=range(len(keys)),yticklabels=labels,xlabel='Contribution to original full-target MAP@12 (%)',title='Ordinary top12: decomposition by target novelty; unavailable targets retained')
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=100,decimals=1))
    ax.legend(loc='lower right',fontsize=8)
    fig.tight_layout();fig.savefig(dest/'ap_contributions.png',dpi=170);fig.savefig(dest/'ap_contributions.svg');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(16,10),sharey=True)
    for ax,mode in zip(axes,['normal','new_only']):
        values=[table[(table.method==key)&(table['mode']==mode)&(table['group']=='new')].available_macro_recall.iloc[0]*100 for key in keys]
        ax.barh(range(len(keys)),values,color='#4c78a8')
        ax.set(yticks=range(len(keys)),yticklabels=labels,xlabel='Macro recall@12 of available NEW targets (%)',title='Original recommendations' if mode=='normal' else 'Exclude all previously purchased items')
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=100,decimals=1))
    fig.suptitle('Same eligible users for every method; TDM keeps native beam64; IDGNN new-only scores are zero ties')
    fig.tight_layout();fig.savefig(dest/'new_item_recall.png',dpi=170);fig.savefig(dest/'new_item_recall.svg');plt.close(fig)
    lines=['# Повторные и новые товары: диагностика всех методов','',
        'Три прежние test-недели,5519наблюдений/4548покупателей. Никакого нового обучения, '
        'настройки моделей или API-запросов. Исходные предсказания воспроизведены и сохранены.', '',
        '## Доступность целей в каталоге', '',
        '| Группа | Всего целей | Доступно | Вне каталога | Покрытие | Пользователей-недель с целями | Из них только недоступные |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for c in coverage:
        if c['targets']==0:continue
        lines.append(f"| {audit.LABELS[c['group']]} | {c['targets']} | {c['available']} | {c['unavailable']} | {100*c['coverage']:.2f}% | {c['users_with_targets']} | {c['users_only_unavailable']} |")
    lines+=['','Группы определяются относительно всей доступной исходной истории H&M '
        'строго до cutoff включительно, включая покупки вне каталога и до начала ограниченной '
        'истории моделей. Оригинальные признаки/история моделей при инференсе не расширялись. '
        'Категория — product_type_no, знакомый продукт — product_code. Производитель не предполагается.', '',
        'Все будущие покупки сохранены. Недоступные цели остаются в знаменателях обычных '
        'метрик. Условные метрики по доступным целям показаны отдельно, на одном и том же '
        'наборе пользователей для всех методов. Пользователи без доступных целей не становятся '
        '«идеальными»: в полном recall они дают0, в условной метрике не участвуют, их число указано.', '',
        '## Обычный top12: откуда берётся MAP', '',
        '| Метод | Исходный MAP,% | Повторные: вклад, п.п. | Доля MAP от повторных | Новые: вклад, п.п. | Recall новых, все цели,% | Recall новых, доступные цели,% |',
        '|---|---:|---:|---:|---:|---:|---:|']
    ranked=normal.sort_values('map',ascending=False)
    for row in ranked.itertuples():
        r=table[(table.method==row.method)&(table['mode']=='normal')&(table['group']=='repeat')].iloc[0]
        n=table[(table.method==row.method)&(table['mode']=='normal')&(table['group']=='new')].iloc[0]
        share=r.ap_contribution/row.map if row.map else 0
        lines.append(f'| {row.label} | {100*row.map:.4f} | {100*r.ap_contribution:.4f} | {100*share:.2f}% | {100*n.ap_contribution:.4f} | {100*n.macro_recall:.4f} | {100*n.available_macro_recall:.4f} |')
    lines+=['','Вклады групп сохраняют исходный знаменатель AP по всем целям и precision '
        'на исходных позициях. Сумма пяти непересекающихся вкладов точно равна исходному MAP. '
        'Доля MAP — доля метрики, а не доля будущих покупок. Recall усредняется по '
        'наблюдениям с хотя бы одной целью соответствующей группы. Micro recall и hit rate '
        'также сохранены в metrics.csv; подробные строки — per_user_metrics.parquet.', '',
        '## Только ранее не покупавшиеся товары', '',
        '| Метод | Recall новых, все цели,% | Recall новых, доступные,% | Hit rate новых, все цели,% | MAP по новым целям,% | Условный MAP доступных новых,% |',
        '|---|---:|---:|---:|---:|---:|']
    new=table[(table['mode']=='new_only')&(table['group']=='new')].sort_values('available_macro_recall',ascending=False)
    for row in new.itertuples():
        lines.append(f'| {row.label} | {100*row.macro_recall:.4f} | {100*row.available_macro_recall:.4f} | {100*row.hit_rate:.4f} | {100*row.map:.4f} | {100*row.available_map:.4f} |')
    lines+=['','Новые top12 получены после исключения всех ранее купленных candidate ID '
        'из полных скоров GNN/Recformer и полного повторного инференса сохранённых деревьев. '
        'Это не обрезание готового top12. TDM сохраняет исходное внутреннее отсечение beam64; '
        'маска применяется перед финальным выбором из всех достигнутых листьев. Цели, '
        'не достигнутые beam, остаются в знаменателе и считаются пропусками.', '',
        'У ID-GNN все содержательные локальные скоры относятся к прошлым покупкам. '
        'После исключения прошлых покупок оставшиеся рекомендации с нулевыми скорами '
        'разрешаются поID. Эти строки измерены, но не являются персональным ранжированием '
        'новых товаров. См. positive_new_scores в model_verification.json.', '',
        '## Новые варианты, знакомые и новые типы', '',
        '| Метод | Режим | Новый вариант: доступный recall,% | Новый продукт знакомого типа,% | Новый тип,% |',
        '|---|---|---:|---:|---:|']
    for key in ranked.method:
        for mode in ['normal','new_only']:
            values=[]
            for group in ['new_variant','new_product_known_type','new_type']:
                value=table[(table.method==key)&(table['mode']==mode)&(table['group']==group)].available_macro_recall.iloc[0]
                values.append('—' if pd.isna(value) else f'{100*value:.4f}')
            label=table[table.method==key].label.iloc[0]
            lines.append('| '+label+' | '+mode+' | '+' | '.join(values)+' |')
    lines+=['','## Неопределённость и ограничения', '',
        'paired_novelty_contrasts.csv содержит5000парныхbootstrap по исходным покупателям '
        'для сравнения нового ContextGNN с прежним ContextGNN,ID-GNN,Recformer,manual,H008/H009 '
        'по recall доступных новых товаров и MAP всех новых целей. Это условные интервалы '
        'для этих недель/моделей, без поправки за множество сравнений; не новые seeds или '
        'независимое подтверждение. Типы товаров — более узкая группировка, чем «одежда вообще». '
        'Статические атрибуты взяты из снимка H&M; историческая доступность снимка не доказана.', '',
        '![Вклады в MAP](ap_contributions.png)','![Recall новых товаров](new_item_recall.png)','']
    (dest/'report_ru.md').write_text('\n'.join(lines),encoding='utf-8')
    write(dest/'summary.json',dict(status='pending_visual_review',coverage=coverage,
        normal=table[(table['mode']=='normal')&(table['group'].isin(['all','repeat','new']))].replace({np.nan:None}).to_dict('records'),
        new_only=new.replace({np.nan:None}).to_dict('records'),principal_contrasts=principal,
        references_unchanged=True,models=15,folds=3,observations=5519))
    record('novelty_report_generated','Novelty audit tables and two figures generated for all methods; inaccessible future targets retained, conditional diagnostics separated. Awaiting visual review.',audit.RUN,status='pending_visual_review',artifacts=str((dest/'report_ru.md').relative_to(ROOT)))
    print(new[['label','macro_recall','available_macro_recall','map']].to_string(index=False),flush=True)


if __name__=='__main__':main()
