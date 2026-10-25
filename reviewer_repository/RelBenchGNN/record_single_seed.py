"""Persist the user's reduction of the experiment to seed 42."""
from tracking import record

record("protocol_change", "Пользователь сократил эксперимент до одного seed 42 для ускорения. Готовый ID-GNN сохранён; далее независимый инференс и два ручных baseline только seed 42. Статья: среднее пяти запусков; локальный разброс не оценивается.",
       selected_seeds=[42], previous_seeds=[42, 43, 44, 45, 46],
       artifacts="RelBenchGNN/experiment_plan.json")
for seed in range(43, 47):
    for prefix in ["hm_idgnn_last", "hm_decision_tree_manual", "hm_lightgbm_manual"]:
        record("run_cancelled", "Дополнительный seed отменён пользователем; существующие артефакты сохранены и исключены из итогового сравнения.",
               f"{prefix}_seed_{seed}_v1", status="cancelled", included_in_comparison=False)
