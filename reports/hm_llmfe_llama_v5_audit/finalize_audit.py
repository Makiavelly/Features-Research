"""Record an executed experiment with proven feature semantics failure; preserve original outputs."""
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
pre=json.loads((HERE/'preaudit.json').read_text())
probes=json.loads((HERE/'semantic_probes.json').read_text())
chosen=next(p for p in probes if p['candidate']==151)
assert chosen['permutation_invariant'] is False and chosen['batch_invariant'] is False
failed=[p['candidate'] for p in probes if p.get('permutation_invariant') is False or p.get('batch_invariant') is False]
comparison=pd.read_csv(HERE/'export/comparison.csv')
flat=pd.read_csv(ROOT/'reports/hm_llmfe_flat_v1_audit/export/comparison.csv')
lines=['# Аудит H&M Llama v5: завершён, но обнаружена ошибка сопоставления признаков','',
    'Источник: features-llama-plus-lightgbm-v3.ipynb. Внутренний протокол — preflight_fulltrain_v5,',
    'интерфейс modify_features(X, history). Это не flat-эксперимент.',
    'Embedded runtimeSHA ноутбука точно совпадают с конфигом архива и локальным evaluator.',
    'Конфиг fingerprint949add5c4fef проверен. Оригинальные ZIP и notebook не изменялись.','',
    '20 технически оценённых программ за154 обращения:134 отказа,103 repair calls,51 новых предложений.',
    '132 отказа на preflight,2 синтаксических. LLM generation time9537.4s (~2ч39мин), не полное время запуска.',
    'Все20 сохранённых кандидатов имеют803377 train пар и совпадающие program/model SHA.',
    'Raw и выбранная модель: независимый повтор4 val/test скорингов дал точные top12/AP/MAP.','',
    '| Модель | Val MAP@12, % | Test MAP@12, % |','|---|---:|---:|']
lines.extend(f'| {r.model} | {100*r.val_map:.5f} | {100*r.test_map:.5f} |' for r in comparison.itertuples())
f=next(r for r in flat.itertuples() if r.model=='LLM-FE flat LightGBM')
lines.append(f'| LLM flat (другой проверенный запуск) | {100*f.val_map:.5f} | {100*f.test_map:.5f} |')
lines+=['','## Подтверждённая смысловая ошибка candidate151','',
    'F имеет RangeIndex строк0..N-1. Результат history.groupby(article_id) имеет индекс ID товара.',
    'Прямое присваивание Series в F сопоставляет ID товара с НОМЕРОМ строки вместо X.article_id.',
    'Аналогично customer_id ошибочно сопоставляется с номером строки.',
    'Сохранение длины/индекса F не обнаруживает эту ошибку. У выбранной модели28 полей:15raw+13generated.','',
    'Проверка128 search пар с одинаковой историей:',
    '- перестановка пар со сбросом технического индекса меняет признаки после обратной перестановки;',
    '- обработка128 строк целиком и двумя блоками64 даёт разные результаты;',
    '- f_article_mean_price отличается от правильного ID-сопоставления у70 из128 пар;',
    '- оба customer-признака отличаются у52 из128 пар; фактический столбец целикомNaN,',
    '  хотя при правильном сопоставлении52 значения должны существовать.','',
    'Из20 технически валидных программ этот probe провалили '+', '.join(map(str,failed))+'.',
    'Остальные не провалили данный ограниченный тест, но это не доказывает полную семантическую корректность.',
    'Ни исправление исходного кода, ни переобучение/выбор другого кандидата по test не выполнялись.','',
    'Правильный принцип, иллюстрация (не новая оценённая программа):',
    '```python',
    "mean_price = history_7day.groupby('article_id')['price'].mean()",
    "F['f_article_mean_price'] = X['article_id'].map(mean_price).to_numpy()",
    '```','',
    'Итог: численные метрики воспроизводимы, но их нельзя интерпретировать как оценку правильно',
    'сформированных13 исторических признаков. Результат отмечен complete_with_alignment_bug.',
    'Для новой версии необходим контроль соответствия ID, перестановки и разбиения строк до обучения.',
    'В flat host выполняет соединения, а preflight проверяет batch-invariance; у выбранного flat-кода',
    'четыре отношения вычисляются по одной строке, поэтому эта конкретная ошибка отсутствует.',
    '', '## Сравнение протоколов','',
    '| Протокол | Обращения | Технически оценено | Доля успеха | Test MAP, % |','|---|---:|---:|---:|---:|',
    '| X + history v5 |154|20|12.99%|0.73457 (ошибка сопоставления)|',
    '| Flat table |23|20|86.96%|0.80095|','',
    'Одинаковыеval1024/test2048 и фиксированные кандидаты; не весь каталог и не полный test.',
    'У flat есть ручные исторические агрегаты и ручной seed; это не чистое сравнение силы LLM.',
    'ID-GNN имеет другой upstream-бюджет. Эти результаты не являются воспроизведением статьи.','',
    '![Метрики](export/comparison.png)','![Поиск](export/search_progress.png)',
    '![Отказы и обучение](export/training_and_rejections.png)']
(HERE/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
result={**pre,'semantic_probes':probes,'chosen_feature_semantics_valid':False,
    'proven_noninvariant_candidates':failed,'comparison':comparison.to_dict('records'),
    'full_catalog':False,'paper_reproduction':False,'new_training_performed':False}
(HERE/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record
winner=next(r for r in comparison.to_dict('records') if r['model']=='LLM-FE LightGBM')
record('hm_llama_v5_semantic_audit',
    'Получен итог v5 из features-llama-plus-lightgbm-v3.ipynb:20 технически оценённых программ за154 calls,134 отказа. '
    'Выбран candidate151, valMAP0.977301%,test0.734573% на общих1024/2048 пользователях. '
    'Но обнаружено неверное pandas-сопоставление: groupby Series поarticle_id/customer_id присвоены вRangeIndex F '
    'безmap/reindex по ID. Перестановка/разбиение128пар меняют признаки;mean_price неверен у70/128, '
    'customer-признаки у52/128. Такой probe провалили кандидаты56,131,147,151. '
    '20 model/program SHA и2 runtimeSHA совпали, независимый replay Raw/selected×val/test точный. '
    'Метрики воспроизводимы, но не означают правильные исторические признаки. '
    'Никакого ремонта/переобучения или нового выбора поtest не было; исходники/ZIP неизменны. '
    'Flat запуск20/23 иtest0.800949% остаётся отдельным экспериментом.',
    run_id='hm_llmfe_llama31_8b_lightgbm_preflight_fulltrain_v5_949add5c4fef',
    status='complete_with_alignment_bug',artifacts='reports/hm_llmfe_llama_v5_audit',
    val_metrics={'map':winner['val_map'],'users':1024,'scope':'shared subset; feature alignment bug'},
    test_metrics={'map':winner['test_map'],'users':2048,'scope':'shared subset; feature alignment bug'},
    llm_calls=154,evaluated_distinct=20,rejected=134,selected_candidate=151,
    chosen_feature_semantics_valid=False,independent_frozen_replay=True,full_catalog=False)
print('Audit recorded; chosen program has confirmed alignment bug.')
