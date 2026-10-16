"""Record audited subset metrics without confusing them with full-catalog/full-test scores."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'RelBenchGNN'))
from tracking import record
audit=json.loads((Path(__file__).parent/'audit.json').read_text())
winner=next(row for row in audit['comparison'] if row['model']=='LLM-FE flat LightGBM')
record('hm_flat_real_run_audited',
    'Реальный flat эксперимент проверен:20 наборов за23 обращения,3 отказа; выбран candidate003. '
    'LLM test MAP0.800949%,Prepared30 0.737375%,Seeded32 0.723351%,Raw15 0.713138%, '
    'manual126 1.862883%,GNN→LGBM1.680568%,ID-GNN2.254944% на общих2048 test пользователях. '
    '20 candidate model/program SHA и7 runtime SHA совпали. Независимый replay4 моделей×val/test '
    'точно совпал. Парный bootstrap10k:LLM−Prepared30+.063574п.п.,95%[+.010718;+.127851]; '
    'к Raw15 интервал пересекает0. Raw15 лучше LLM на val. Качество существенно ниже manual/GNN; '
    'не полный каталог/не полный test. Выбранные4 LLM ratio поверх30base+2ручныхseedlog. '
    'flat_manifest отсутствует вZIP; исходныйbundle и код проверены, локальный кэш дал те же предсказания. '
    'Оригинальный архив не изменён.',
    run_id='hm_llmfe_llama31_8b_lightgbm_flat_fulltrain_v1_aa1ed17300ae',
    status='complete',artifacts='reports/hm_llmfe_flat_v1_audit',
    val_metrics={'map':winner['val_map'],'users':1024,'scope':'shared candidate subset'},
    test_metrics={'map':winner['test_map'],'users':2048,'scope':'shared candidate subset'},
    llm_calls=23,evaluated_distinct=20,rejected=3,selected_candidate=3,
    independent_frozen_replay=True,full_catalog=False,paper_reproduction=False)
