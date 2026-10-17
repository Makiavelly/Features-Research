"""Report exactly20 authored adaptive sets; no claim of model attestation."""
import json
from pathlib import Path
import shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/authored20_v1'


def read(path):return json.loads(Path(path).read_text())


def main():
    audit=read(OUT/'audit.json');assert audit['status']=='passed'
    source=Path(audit['source_directory'])
    own=pd.read_csv(OUT/'comparison.csv')
    previous=pd.read_csv(ROOT/'reports/gpt61sol_python_v1/comparison_all_methods.csv')
    frame=pd.concat([previous,own[own.model=='CodexAuthored20']],ignore_index=True)
    assert frame.model.is_unique
    frame.to_csv(OUT/'comparison_all_methods.csv',index=False)
    names=['Raw15_LightGBM','Qwen7B_LightGBM','GPT61Sol_SQL','GPT61Sol_Python',
           'CodexAuthored20','lightgbm_manual','idgnn','contextgnn']
    labels=['LightGBM: исходные поля','Qwen7B → LightGBM',
            'Провайдер: GPT, SQL → LightGBM','Провайдер: GPT, Python → LightGBM',
            'Эта сессия Codex → LightGBM','LightGBM: ручные признаки','ID-GNN','ContextGNN']
    colors=['#aaaaaa','#577590','#8e44ad','#e67e22','#d73027','#aaaaaa','#aaaaaa','#aaaaaa']
    indexed=frame.set_index('model')
    fig,axes=plt.subplots(1,2,figsize=(15,7))
    for axis,stage in zip(axes,['val','test']):
        values=indexed.loc[names,stage+'_map_percent'].to_numpy()
        axis.barh(labels,values,color=colors)
        for y,v in enumerate(values):axis.text(v+.02,y,f'{v:.3f}%',va='center',fontsize=9)
        axis.set(xlabel='MAP@12 (%)',title='Validation: включает search/confirm' if stage=='val' else 'Test: повторная оценка',
                 xlim=(0,values.max()*1.16));axis.grid(axis='x',alpha=.2)
    fig.suptitle('Те же72813train-пар и каталог5000; контекст и бюджет генерации различаются')
    fig.tight_layout();fig.savefig(OUT/'comparison.png',dpi=160);plt.close(fig)
    # Include every saved method, not only the short eight-method overview.
    full = frame.sort_values('test_map_percent', ascending=True).copy()
    full_labels = full.model.replace({
        'CodexAuthored20': 'Codex: 20 sets (prior history known)',
        'Raw15_LightGBM': 'LightGBM: raw15',
        'GPT61Sol_SQL': 'Provider GPT: SQL + raw15',
        'GPT61Sol_Python': 'Provider GPT: Python + raw15',
        'Qwen7B_LightGBM': 'Qwen7B + LightGBM',
        'Llama8B_LightGBM': 'Llama8B + LightGBM',
        'Qwen14B_LightGBM': 'Qwen14B + LightGBM',
    })
    fig, axes = plt.subplots(1, 2, figsize=(18, max(9, len(full)*.39)), sharey=True,
                             constrained_layout=True)
    y = np.arange(len(full))
    palette = ['#d73027' if name == 'CodexAuthored20' else '#557b9d' for name in full.model]
    for axis, stage in zip(axes, ['val', 'test']):
        values = full[stage+'_map_percent'].to_numpy()
        axis.barh(y, values, color=palette)
        for row, value in enumerate(values):
            axis.text(value+.025, row, f'{value:.3f}%', va='center', fontsize=8)
        axis.set(xlabel='MAP@12 (%)', title='Validation (includes search/confirmation)' if stage=='val' else 'Test (previously inspected)',
                 yticks=y, yticklabels=full_labels.tolist(), xlim=(0, values.max()*1.18))
        axis.grid(axis='x', alpha=.2)
    fig.suptitle('H&M small: all saved methods | same validation/test cohorts\nTraining and generation budgets differ; Codex search was not blind', fontsize=13)
    fig.savefig(OUT/'comparison_all_methods.png', dpi=160)
    fig.savefig(OUT/'comparison_all_methods.svg')
    plt.close(fig)
    trials=pd.read_csv(OUT/'all20_search.csv')
    state=read(source/'state.json')
    selected=audit['selected']
    confirmation={x['call']:100*x['confirmation_map'] for x in selected['confirmation']}
    trials['confirm_map_percent']=trials.call.map(confirmation)
    trials.to_csv(OUT/'all20_metrics.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(13,5))
    palette=['#577590','#43aa8b','#d73027']
    raw_search=float(own[own.model=='Raw15'].iloc[0].search_map_percent)
    for island,color in enumerate(palette):
        subset=trials[trials.island==island]
        x=subset.call.to_numpy();y=subset.search_map_percent.to_numpy()
        axes[0].scatter(x,y,color=color)
        axes[0].step(np.r_[0,x],np.r_[raw_search,np.maximum.accumulate(np.maximum(y,raw_search))],
                     where='post',label=f'Популяция{island}',color=color)
        axes[1].bar(x,y,color=color,label=f'Популяция{island}')
    axes[0].set(xlabel='Номер из20авторских наборов',ylabel='Search MAP@12 (%)',title='Лучшее в каждой популяции')
    axes[0].legend();axes[0].grid(alpha=.2)
    axes[1].set(xlabel='Набор',ylabel='Search MAP@12 (%)',title='Все20, без исключённых результатов')
    axes[1].set_xticks(np.arange(1,21));axes[1].legend(fontsize=8)
    fig.tight_layout();fig.savefig(OUT/'search_progress.png',dpi=160);plt.close(fig)
    ownq=read(OUT/'quality.json')
    providerq=read(ROOT/'reports/gpt61sol_python_v1/quality.json')
    sqlq=read(ROOT/'reports/gpt61sol_small_v2/quality.json')
    qwenq=read(ROOT/'reports/hm_small_llms_v1/quality.json')
    aps={'Codex':np.array(ownq['CodexAuthored20']['test']),
         'Provider Python':np.array(providerq['GPT61Sol']['test']),
         'Provider SQL':np.array(sqlq['GPT61Sol']['test']),
         'Qwen7B':np.array(qwenq['Qwen7B_LightGBM']['test']),
         'Raw15':np.array(ownq['Raw15']['test'])}
    differences=[];rng=np.random.default_rng(42)
    for label in ['Provider Python','Provider SQL','Qwen7B','Raw15']:
        delta=aps['Codex']-aps[label]
        samples=delta[rng.integers(0,len(delta),size=(10000,len(delta)))].mean(1)*100
        differences.append({'comparison':'Codex minus '+label,'difference_pp':float(delta.mean()*100),
                            'ci95_low_pp':float(np.quantile(samples,.025)),'ci95_high_pp':float(np.quantile(samples,.975)),
                            'better':int((delta>0).sum()),'tied':int((delta==0).sum()),'worse':int((delta<0).sum())})
    pd.DataFrame(differences).to_csv(OUT/'paired_bootstrap.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(12,5))
    for label in ['Codex','Provider Python','Qwen7B','Raw15']:
        values=aps[label]
        axes[0].hist(values[values>0]*100,bins=np.linspace(0,100,21),histtype='step',label=label)
        axes[1].bar(label,100*np.mean(values==0))
    axes[0].set(xlabel='AP@12 пользователя (%) среди AP>0',ylabel='Пользователи');axes[0].legend(fontsize=8)
    axes[1].set(ylabel='Пользователи с AP=0 (%)',ylim=(0,100));axes[1].tick_params(axis='x',rotation=20)
    fig.tight_layout();fig.savefig(OUT/'test_histograms.png',dpi=160);plt.close(fig)
    shutil.copy2(source/'lightgbm_training.png',OUT/'lightgbm_training.png')
    winner=Path(selected['directory'])
    selected_program=(winner/'program.py').read_text()
    lines=['# H007: ровно20 наборов от текущей сессии Codex','',
           '**Реальный эксперимент, не smoke. Точная модель этой сессии не аттестована.**',
           'Текущая сессия самостоятельно написала общий Python код и20адаптивных решений; внешних API запросов0.',
           'Ровно20 новых обученных LightGBM,20 различных числовыхtrain-матриц. Raw контроль переиспользован изH006, не является21-м авторским набором.',
           f"Три популяции: {audit['island_counts']}. Лучший родитель своей популяции проверен для каждого шага; "
           'цепочка хешей подтверждает фиксацию до получения search-оценки.',
           f"Победитель поconfirmation: набор{selected['call']} (null=raw). Итоговые прогнозы независимо пересчитаны из замороженных моделей.",'',
           '| Метод | Validation MAP,% | Heldout88 MAP,% | Test MAP,% |','|---|---:|---:|---:|']
    for name,label in zip(names,labels):
        row=indexed.loc[name]
        lines.append(f'| {label} | {row.val_map_percent:.6f} | {row.heldout_val_map_percent:.6f} | {row.test_map_percent:.6f} |')
    lines+=['','## Все20результатов','', '| № | Популяция | Родитель | Признаков | Search MAP,% | Confirmation MAP,% |','|---:|---:|---:|---:|---:|---:|']
    for row in trials.itertuples():
        parent='raw' if pd.isna(row.parent_call) else str(int(row.parent_call))
        confirm='—' if pd.isna(row.confirm_map_percent) else f'{row.confirm_map_percent:.6f}'
        lines.append(f'| {row.call} | {row.island} | {parent} | {row.features} | {row.search_map_percent:.6f} | {confirm} |')
    lines+=['','Подробные решения и обоснования до оценки:','']
    for trial in state['trials']:
        path=source/'codex_authored20/candidates'/f"candidate_{trial['call']:03d}"/'proposal.json'
        proposal=read(path)
        lines.append(f"- {trial['call']}: {proposal['description']}. {proposal['rationale']}")
    lines+=['','## Равные условия downstream','',
            '72813 фиксированных train-пар/4804user-times/8cutoffs; LightGBM binary150/31leaves/4CPU/seed42, '
            'до36новых признаков + те же15raw, точные источникиworker/FeatureEngine/валидатораH006v2.',
            'Search128×весь каталог5000 направляет адаптацию. После20наборов top3search+raw сравниваются на других88confirmationпользователях. '
            'Победитель зафиксирован до heldout88/val304/test250. Test не использован для выбора.',
            'Проверены пустая история, отсутствующие группы, порядок строк, batching, числовая уникальность всех20матриц. '
            'Синтетические эталоны проверяют счётчики, цены/квантили, возраст, каналы, затухание и граф категорий; не обучают дополнительные модели.',
            '', '## Что нельзя заключать','',
            'Это не аттестация эталонной GPT-6.1 Sol. Ни имя текущего движка, ни веса провайдера не подтверждаются метриками.',
            'Я знаю историю прошлых экспериментов; контекст текущей сессии, использование инструментов и объём кода отличаются '
            'от провайдерского промпта и2048выходныхтокенов. Полной эквивалентности бюджета генерации нет. '
            'Популяционные родители независимы, но внутренний контекст этой сессии не разделён на3изолированные LLM.',
            'Все20 были написаны и оценены в явной последовательности. Предварительные неоценённые черновики сохранены отдельно; '
            'скрытого перебора других моделей/гиперпараметров не проводилось.',
            'У провайдерского Python было20оценённых программ, но18числовыхматриц; здесь20/20. '
            'Сравнение отражает весь процесс поиска, не изолирует только свойства языковой модели.',
            'Одинseed и250ранее просмотренныхtest-пользователей. Paired bootstrap исследовательский, не неопределённость между запусками. '
            'Большая разница результатов сама по себе не доказывает подмену модели.',
            'Токены/время генерации текущей сессии не измерены. Нулевыеgenerated_tokens/seconds в совместимыхtrial-записях '
            'означают отсутствие метрики внешнегоAPI, а не нулевые реальные затраты на генерацию.',
            '', '## Парные интервалы разницы наtest','',
            '| Сравнение | Разница, п.п. | 95% интервал, п.п. |','|---|---:|---|']
    for delta in differences:
        lines.append(f"| {delta['comparison']} | {delta['difference_pp']:+.6f} | [{delta['ci95_low_pp']:+.6f}; {delta['ci95_high_pp']:+.6f}] |")
    lines+=['','## Код выбранного набора','', '```python',selected_program,'```','',
            '![Общее сравнение](comparison.png)','', '![Поиск](search_progress.png)','',
            '![Гистограммы](test_histograms.png)','', '![LightGBM](lightgbm_training.png)']
    (OUT/'report.md').write_text('\n'.join(lines),encoding='utf-8')
    result={'status':'audited','run_id':audit['run_id'],'comparison':frame.to_dict('records'),
            'exactly20':True,'api_requests':0,'identity_attested':False,'selected_call':selected['call'],
            'bootstrap':differences,'limitations':audit['limitations']}
    (OUT/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(own.to_string(index=False));print(pd.DataFrame(differences).to_string(index=False))


if __name__=='__main__':main()
