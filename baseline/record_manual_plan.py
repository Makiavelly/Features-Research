import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "RelBenchGNN"))
from tracking import record

record("user_request", "Нужно сравнение ID-GNN с локальной моделью дерева на ручных признаках, а также отдельные значения из статьи и фактические локальные результаты.")
record("manual_adaptation", "Создано 126 ручных признаков: адаптированное подмножество экспертных user-churn/item-sales SQL плюс признаки пары. Это наша адаптация, не опубликованный экспертный ранжирующий набор.",
       "hm_manual_tree_pipeline_v1", status="pending", feature_count=126, artifacts="baseline/MANUAL_BASELINE.md",
       train_user_times=50000, tuning_validation_users=10000,
       evaluation="full validation/test, exact respective GNN candidate pool",
       published_lightgbm_raw_map_percent={"val": .44, "test": .38}, published_idgnn_map_percent={"val": 2.64, "test": 2.81})
record("feature_tests", "Тесты ручных признаков пройдены: cutoff, исключение будущих транзакций, отсутствие ID/метки во входах, одна строка на пару.")
for kind in ["decision_tree", "lightgbm"]:
    for seed in range(42, 47):
        record("planned_run", f"Запланирован {kind} на ручных признаках после освобождения ресурсов GNN", f"hm_{kind}_manual_seed_{seed}_v1",
               status="pending", seed=seed, artifacts=f"baseline/results/manual_v1/{kind}/seed_{seed}")
