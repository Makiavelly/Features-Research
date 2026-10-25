"""Compare audited complete-Python generation with the preceding SQL run."""
import json
from pathlib import Path
import shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/gpt61sol_python_v1'


def read(path):return json.loads(Path(path).read_text())


def main():
    audit=read(OUT/'audit.json')
    review=read(OUT/'validator_review.json')
    numeric=read(OUT/'numeric_reference_verification.json')
    diversity=read(OUT/'feature_diversity.json')
    assert audit['status']=='passed' and review['status']=='passed'
    assert numeric['status']==diversity['status']=='passed'
    source=Path(audit['source_directory'])
    current=pd.read_csv(OUT/'comparison.csv')
    historical=pd.read_csv(ROOT/'reports/h003_small_v1/comparison_all_methods.csv')
    sql=pd.read_csv(ROOT/'reports/gpt61sol_small_v2/comparison.csv')
    sql=sql[sql.model=='GPT61Sol'].assign(model='GPT61Sol_SQL')
    python=current[current.model=='GPT61Sol'].assign(model='GPT61Sol_Python')
    combined=pd.concat([historical,sql,python],ignore_index=True)
    assert combined.model.is_unique
    combined.to_csv(OUT/'comparison_all_methods.csv',index=False)
    order=['Raw15_LightGBM','Qwen7B_LightGBM','h003c','GPT61Sol_SQL','GPT61Sol_Python',
           'lightgbm_manual','idgnn','contextgnn']
    labels=['LightGBM: исходные 15 полей','Qwen7B → LightGBM (JSON)',
            'Qwen7B H003C → LightGBM (JSON)','GPT-6.1 Sol → LightGBM (SQL)',
            'GPT-6.1 Sol → LightGBM (Python)','LightGBM: ручные признаки','ID-GNN','ContextGNN']
    index=combined.set_index('model')
    colors=['#999999','#577590','#43aa8b','#8e44ad','#e67e22','#999999','#999999','#999999']
    fig,axes=plt.subplots(1,2,figsize=(15,7))
    for axis,stage in zip(axes,['val','test']):
        values=index.loc[order,stage+'_map_percent'].to_numpy()
        axis.barh(labels,values,color=colors)
        for y,v in enumerate(values):axis.text(v+.02,y,f'{v:.3f}%',va='center',fontsize=9)
        axis.set(xlabel='MAP@12 (%)',xlim=(0,values.max()*1.16),
                 title='Validation (включает search/confirm)' if stage=='val' else 'Test: повторная оценка')
        axis.grid(axis='x',alpha=.2)
    fig.suptitle('Small-v1: те же train-пары, пользователи и каталог5000; интерфейсы различаются')
    fig.tight_layout();fig.savefig(OUT/'comparison.png',dpi=160);plt.close(fig)
    stats=audit['stats']
    matrix_by_call={r['call']:r for r in diversity['rows']}
    confirmation_calls=[c['call'] for c in audit['selected']['confirmation'] if c['call'] is not None]
    confirmation_distinct=len({matrix_by_call[c]['ordered_float32_sha256'] for c in confirmation_calls})
    sqlstats=read(ROOT/'reports/gpt61sol_small_v2/audit.json')['stats']
    efficiency=[]
    for name,st in [('GPT SQL',sqlstats),('GPT Python',stats)]:
        efficiency.append(dict(model=name,calls=st['calls'],valid=st['statuses'].get('valid',0),
                               rejected=st['statuses'].get('rejected',0),duplicate=st['statuses'].get('duplicate',0),
                               outside_pool=st.get('outside_corrected_pool',0),
                               api_failures=st.get('api_failures_count',0),minutes=st['generation_minutes']))
    eff=pd.DataFrame(efficiency)
    eff.to_csv(OUT/'generation_efficiency.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(11,5))
    bottom=np.zeros(2)
    for col,color in [('valid','#43aa8b'),('rejected','#f3722c'),('duplicate','#f9c74f'),
                      ('outside_pool','#999999'),('api_failures','#577590')]:
        values=eff[col].to_numpy()
        axes[0].bar(eff.model,values,bottom=bottom,label=col,color=color);bottom+=values
    axes[0].set(ylabel='Фактические API POST',ylim=(0,max(bottom)*1.15),title='Цель: 20 оценённых программ')
    axes[0].legend(fontsize=8)
    axes[1].bar(eff.model,eff.minutes,color=['#8e44ad','#e67e22'])
    axes[1].set(ylabel='Минуты',title='Успешные API ответы: время генерации')
    fig.tight_layout();fig.savefig(OUT/'generation_efficiency.png',dpi=160);plt.close(fig)
    own=read(OUT/'quality.json')
    sqlq=read(ROOT/'reports/gpt61sol_small_v2/quality.json')
    qwen=read(ROOT/'reports/hm_small_llms_v1/quality.json')
    aps={'GPT Python':np.array(own['GPT61Sol']['test']),
         'GPT SQL':np.array(sqlq['GPT61Sol']['test']),
         'Raw15':np.array(own['Raw15']['test']),
         'Qwen7B JSON':np.array(qwen['Qwen7B_LightGBM']['test'])}
    intervals=[]
    rng=np.random.default_rng(42)
    for other in ['GPT SQL','Raw15','Qwen7B JSON']:
        difference=aps['GPT Python']-aps[other]
        values=difference[rng.integers(0,len(difference),size=(10000,len(difference)))].mean(1)*100
        intervals.append(dict(comparison='GPT Python minus '+other,difference_pp=float(difference.mean()*100),
                              ci95_low_pp=float(np.quantile(values,.025)),ci95_high_pp=float(np.quantile(values,.975)),
                              better=int((difference>0).sum()),tied=int((difference==0).sum()),worse=int((difference<0).sum())))
    pd.DataFrame(intervals).to_csv(OUT/'paired_test_bootstrap.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(11,5))
    for label,values in aps.items():
        axes[0].hist(values[values>0]*100,bins=np.linspace(0,100,21),histtype='step',label=label)
        axes[1].bar(label,100*np.mean(values==0))
    axes[0].set(xlabel='AP@12 пользователя (%) среди AP>0',ylabel='Пользователи')
    axes[0].legend(fontsize=8)
    axes[1].set(ylabel='Пользователи с AP=0 (%)',ylim=(0,100))
    axes[1].tick_params(axis='x',rotation=20)
    fig.tight_layout();fig.savefig(OUT/'test_histograms.png',dpi=160);plt.close(fig)
    fig,axis=plt.subplots(figsize=(10,5))
    for name,root,arm,color in [('GPT SQL',Path(read(ROOT/'reports/gpt61sol_small_v2/audit.json')['source_directory']),'gpt61sol_full_sql','#8e44ad'),
                                ('GPT Python',source,'gpt61sol_python','#e67e22')]:
        trials=read(root/arm/'search_state.json')['trials']
        valid=[t for t in trials if t['status']=='valid']
        x=[t['call'] for t in valid];y=np.array([t['score'] for t in valid])*100
        axis.scatter(x,y,color=color,alpha=.5)
        axis.step(x,np.maximum.accumulate(y),label=name,color=color,where='post')
    axis.set(xlabel='Номер ответа модели (HTTP ошибки отдельно)',ylabel='Search MAP@12 (%)',title='Поиск; финальный выбор использует confirmation88')
    axis.legend();axis.grid(alpha=.2)
    fig.tight_layout();fig.savefig(OUT/'search_progress.png',dpi=160);plt.close(fig)
    result={'run_id':audit['run_id'],'status':'audited','stats':stats,'validator_review':review,
            'numeric_reference':numeric,'feature_diversity':diversity,
            'comparison':combined.to_dict('records'),'bootstrap':intervals,
            'limitations':['One seed and previously inspected250-user test',
                           'SQL/Python prompts and example/interface differ; model and downstream/data matched',
                           'Conservative AST dedup does not guarantee numerically distinct features']}
    (OUT/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    gpt=python.iloc[0]
    shutil.copy2(source/'lightgbm_training.png',OUT/'lightgbm_training.png')
    lines=['# H006: GPT-6.1 Sol пишет полную Python-функцию','',
           'Реальный эксперимент, не smoke. Все итоговые прогнозы независимо пересчитаны из замороженных моделей.',
           f"API-запросов: {stats['calls']}; оценённых программ: {stats['statuses'].get('valid',0)}; "
           f"отказов по контракту кода: {stats['statuses'].get('rejected',0)}; дубликатов по AST: {stats['statuses'].get('duplicate',0)}; "
           f"ошибок API отдельно: {stats.get('api_failures_count',0)}.",
           f"Выбран ответ {stats['selected_call']} (null=raw), validation MAP={gpt.val_map_percent:.6f}%, "
           f"heldout88={gpt.heldout_val_map_percent:.6f}%, test={gpt.test_map_percent:.6f}%.",'',
           '| Метод | Validation MAP,% | Heldout88 MAP,% | Test MAP,% |','|---|---:|---:|---:|']
    for name,label in zip(order,labels):
        row=index.loc[name]
        lines.append(f'| {label} | {row.val_map_percent:.6f} | {row.heldout_val_map_percent:.6f} | {row.test_map_percent:.6f} |')
    trials=read(source/'gpt61sol_python/search_state.json')['trials']
    search_by_call={t['call']:t['score'] for t in trials if t['status']=='valid'}
    search_by_call[None]=float(current[current.model=='Raw15'].iloc[0].search_map_percent)/100
    candidates=[{'call':c['call'],'search_map_percent':100*search_by_call[c['call']],
                 'confirmation_map_percent':100*c['confirmation_map']} for c in audit['selected']['confirmation']]
    pd.DataFrame(candidates).to_csv(OUT/'selection_candidates.csv',index=False)
    lines+=['','## Search и confirmation','',
            'Метрика одна — MAP@12; пользователи разные. Search:128 пользователей, каждый набор, '
            'оценка возвращается LLM. Confirmation: другие88 пользователей, толькоtop3search+raw после завершения '
            'поиска; эти оценки LLM не получает. Победитель выбирается поconfirmation, test не участвует.',
            '', '| Ответ | Search MAP,% | Confirmation MAP,% |','|---|---:|---:|']
    for candidate in candidates:
        label='Raw15' if candidate['call'] is None else str(candidate['call'])
        lines.append(f"| {label} | {candidate['search_map_percent']:.6f} | {candidate['confirmation_map_percent']:.6f} |")
    difference=intervals[0]
    lines+=['','## Неопределённость разницы','',
            f"Python минус SQL на test: {difference['difference_pp']:+.6f} п.п.; "
            f"исследовательский 95% парный bootstrap-интервал [{difference['ci95_low_pp']:+.6f}; {difference['ci95_high_pp']:+.6f}] п.п.",
            'Интервал включает ноль. Более высокий результат этого прогона не устанавливает устойчивое превосходство '
            'Python-интерфейса. Полные сравнения с raw/Qwen — paired_test_bootstrap.csv.']
    lines+=['','## Проверка валидатора','',
            f"Перед возобновлением v2 пройдены {audit['validator_regression']['checks_count']} регрессионных проверок (до исходного запуска28): корректный pandas/NumPy, helper-функции, константы, "
            'merge/MultiIndex, ошибки синтаксиса/схемы/индекса, сопоставление Python/SQL и отсутствие будущих покупок.',
            f"После генерации проверены все {review['calls_reviewed']} ответов: "+json.dumps(review['counts'],ensure_ascii=False)+'.',
            'Принятые программы дополнительно проверены в прежнем ограниченном worker: '
            'пустая история, отсутствующие группы, нестандартный индекс, permutation/batching. '
            'Неограниченный exec модельного кода отклонён автоматической проверкой безопасности и не выполнялся; '
            'независимые числовые эталоны написаны аудитором, не моделью.',
            'Отказы разобраны отдельно в validator_review.json. Тесты не доказывают отсутствие всех возможных дефектов.',
            'Независимые аудиторские SQL эталоны подтвердили все11признаковcall3 и17признаковcall5 '
            'на8train-cutoffs. Кроме того, все12признаков выбранногоcall10 полностью выражены SQL: '
            'на всех72813train-парах подтверждено точное равенство float32 значений. '
            'Это прямой пример того, что преимущество не связано с выразительностью Python. '
            'Остальные формулы не объявляются автоматически доказанными этими примерами.',
            'Дополнительный аудит до итогового отбора обнаружил другой порядок тех же столбцов на пустой истории в call5. '
            'v2 выравнивает столбцы по именам и проверяет empty/absent до обучения. Исходный v1 сохранён, '
            'API-бюджет не обнулён, имеющиеся ответы перенесены без повторной генерации. '
            'Переиспользованные модели проверены на совпадение матриц по8train-срезам; это продолжение одного потока, не независимый прогон.',
            '', '## Разнообразие признаков','',
            'Цель поиска —20структурно различных оценённых Python программ. Это не гарантия20различных числовых матриц.',
            f"По всем72813train-строкам: {diversity['groups']['ordered_float32_sha256']['distinct']} различных матриц с учётом порядка столбцов; "
            f"{diversity['groups']['column_multiset_sha256']['distinct']} различных мультимножеств числовых столбцов без учёта имён/порядка.",
            'Совпадающие группы: '+json.dumps(diversity['groups'],ensure_ascii=False),
            f'В фактический confirmation вошли ответы {confirmation_calls}: {confirmation_distinct} различных числовых матриц.',
            'Дедупликация по AST консервативна и может пропускать эквивалентные программы. '
            'Это уменьшает эффективный бюджет поиска; одинаковые варианты могут занять несколько мест вtop3. '
            'Диагностика вычислена после заморозки выбора и не используется для переотбора поtest.',
            'Аудит обнаружил также неточность логаresume: уcall8 сохранённыйprompt был заменён реконструированнымv2 текстом, '
            'который не отправлялся провайдеру. Реальныйprompt восстановлен из неизменногоrequest.json '
            '(он совпадает с сохранённымv1), неотправленный текст сохранён отдельно. '
            'Модель, данные, отбор и метрики не изменялись; деталиprompt_log_reconciliation.json в исходном каталоге.',
            '', '## Условия и ограничения','',
            'Те же72813 пары / LightGBM150/31/4CPU / raw15 / seed42 / 3популяции / 20наборов / до300фактическихPOST / до3repair.',
            'Search128×каталог5000 → top3+raw → confirmation88 → frozen heldout88/val304/test250. '
            'Raw модель и прогнозы побайтно совпали с предыдущими экспериментами.',
            'Модель/API/sampling как SQL: gpt-6.1-sol, temperature0.8, top_p1, reasoning_effortlow, '
            'max_tokens2048, seed42+номер_ответа−1 запрошен. Реализация и гарантии seed провайдера не контролируются.',
            'В Python до36 новых признаков; исходные15 добавляет host. LLM видит схему и3training-примера, '
            'полную прошлую историю обрабатывает её код. Саму LLM не дообучаем.',
            'Язык, формат интерфейса и пример в промпте отличаются от SQL; один прогон не изолирует их причинный эффект.',
            'Большинство полученных признаков одинаково выразимы SQL и Python. Эксперимент проверяет поиск через другой интерфейс, '
            'а не превосходство языка. Одинаковые числовые матрицы при тех же настройках дают то же обучение LightGBM.',
            'Test ранее просмотрен. Paired bootstrap10k по пользователям исследовательский; это не multi-seed uncertainty.',
            'Исторический Qwen использовал JSON DSL, а baselines имели другие бюджеты настройки. '
            'Корректный исполняемый код не гарантирует полезные признаки.',
            'SQL столбец — исправленная оценка исходного потока без новых генераций; 2 исходных ответа вне correctedpool сохранены.',
            'HTTP502 не считается ошибкой модели/валидатора. Usage и время генерации охватывают полученные ответы; '
            'денежная стоимость и списание за ошибочный HTTP запрос неизвестны.',
            '', '## Выбранный Python','', '```python',audit['selected_Python'],'```','',
            '![Сравнение](comparison.png)','', '![Вызовы](generation_efficiency.png)','',
            '![Поиск](search_progress.png)','', '![Гистограммы](test_histograms.png)','',
            '![Обучение LightGBM](lightgbm_training.png)']
    (OUT/'report.md').write_text('\n'.join(lines),encoding='utf-8')
    print(combined[combined.model.isin(order)].to_string(index=False))
    print(pd.DataFrame(intervals).to_string(index=False))


if __name__=='__main__':main()
