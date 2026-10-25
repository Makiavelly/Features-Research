"""Compare frozen Qwen and Llama predictions on the identical Kaggle-exported rows/pools."""
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from worker import map_at_12

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'reports/llama_vs_qwen_shared_subset'
OUT.mkdir(parents=True,exist_ok=True)
bundle=ROOT/'data/kaggle_hm_llmfe_fulltrain_v2'
manifest=json.loads((bundle/'manifest.json').read_text())
qwen_run=ROOT/'LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1'
selection=json.loads((qwen_run/'selected.json').read_text())
chosen=qwen_run/'candidates'/Path(selection['directory']).name
rows=[]
for split in ['val','test']:
    indices=np.asarray(manifest['splits'][split]['original_row_indices'])
    truth=pd.read_parquet(bundle/f'{split}_targets.parquet')
    original=pd.read_parquet(ROOT/f'data/rel-hm/tasks/user-item-purchase/{split}.parquet')
    pd.testing.assert_frame_equal(original.iloc[indices].reset_index(drop=True),truth)
    pool=pd.read_parquet(ROOT/f'RelBenchGNN/results/seed_42/inference/{split}_candidates.parquet').iloc[indices].reset_index(drop=True)
    assert np.array_equal(pool.customer_id.to_numpy(),truth.customer_id.to_numpy())
    predictions=np.load(chosen/f'shared_{split}_predictions.npy')[indices]
    assert all(np.isin(p,c).all() and len(np.unique(p))==12 for p,c in zip(predictions,pool.candidates))
    value,ap=map_at_12(predictions,truth.article_id)
    np.save(OUT/f'qwen_h002_{split}_user_ap.npy',ap)
    rows.append({'model':'Qwen H002 → LightGBM','split':split,'map':value,'users':len(truth)})
flat=pd.read_csv(ROOT/'reports/hm_llmfe_flat_v1_audit/export/comparison.csv')
for row in flat.itertuples():
    for split in ['val','test']:
        rows.append({'model':row.model,'split':split,'map':getattr(row,split+'_map'),
                     'users':len(pd.read_parquet(bundle/f'{split}_targets.parquet'))})
comparison=pd.DataFrame(rows).pivot(index='model',columns='split',values='map').reset_index()
comparison.to_csv(OUT/'comparison.csv',index=False)
lines=['# Qwen и Llama: одинаковые пользователи и кандидаты','',
    'Qwen H002: candidate060, ранее выбран по validation, без нового отбора или обучения.',
    'Его сохранённые полные предсказания ограничены исходными индексами из Kaggle manifest.',
    'Порядок customer_id, цели и принадлежность top12 общим кандидатам проверены.',
    'Validation1024/test2048 — те же строки, что в Llama flat.','',
    '| Модель | Val MAP@12, % | Test MAP@12, % |','|---|---:|---:|']
lines.extend(f'| {r.model} | {100*r.val:.5f} | {100*r.test:.5f} |' for r in comparison.itertuples())
lines+=['','Это сравнение конвейеров, не изолированный тест силы языковых моделей.',
    'У Qwen SQL-агрегации/формулы по истории и иной контекст истории/поиска; у flat Llama',
    '15 ручных исторических агрегатов+Python преобразования. В обоих случаях деревья учились',
    'на803377 парах; прежние отличия протоколов/отбора остаются.',
    'V5 Llama с ошибкой ID-сопоставления не рассматривается как корректный feature-engineering результат.']
(OUT/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(comparison.to_json(orient='records',force_ascii=False,indent=2))
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record
q=next(row for row in rows if row['model']=='Qwen H002 → LightGBM' and row['split']=='test')
record('llama_qwen_common_subset_comparison',
    'Пересчитан замороженный Qwen H002 candidate060 на тех же1024val/2048test пользователях и ID-GNN пулах, '
    'что Llama flat. Строки/цели/customerIDs/принадлежностьtop12 проверены. Без нового обучения или выбора поtest. '
    f"Qwen subset testMAP={100*q['map']:.6f}%;Llama flat0.800949%. Это сравнение разных конвейеров, не чистой силыLLM.",
    artifacts='reports/llama_vs_qwen_shared_subset',qwen_subset_test_map=q['map'],test_users=2048)
