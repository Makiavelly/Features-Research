"""Apply the user's one-seed decision consistently across local reports and baselines."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for name in ["RelBenchGNN/build_report.py", "RelBenchGNN/monitor.py", "baseline/run_manual_tree.py"]:
    path = ROOT / name
    source = path.read_text(encoding="utf-8")
    source = source.replace("from tracking import record", "from tracking import record\nfrom experiment_plan import selected_seeds\nSEEDS = selected_seeds()")
    source = source.replace("range(42, 47)", "SEEDS")
    if name.endswith("build_report.py"):
        source = source.replace("/5 completed", "/{len(SEEDS)} completed")
        source = source.replace("== 5", "== len(SEEDS)")
        source = source.replace("/5.", "/{len(SEEDS)}.")
        source = source.replace("statistics.pstdev(val_values) if val_values else None", "statistics.pstdev(val_values) if len(val_values) > 1 else None")
        source = source.replace("statistics.pstdev(test_values) if test_values else None", "statistics.pstdev(test_values) if len(test_values) > 1 else None")
        source = source.replace("if records else None} for kind", "if len(records) > 1 else None} for kind")
        source = source.replace("if records else None,\n        \"test_std_percent\"", "if len(records) > 1 else None,\n        \"test_std_percent\"")
        source = source.replace("if val_values:\n        lines +=", "if len(val_values) > 1:\n        lines +=")
        source = source.replace("Среднее ID-GNN считается только по завершённым запускам; до 5/5 оно промежуточное.", "Локальный эксперимент использует один seed 42 по просьбе пользователя. Статья сообщает среднее пяти запусков; локальный разброс по seeds не оценён.")
        source = source.replace("seeds 42–46 выбраны нами", "seed 42 выбран нами; число запусков сокращено пользователем до одного")
    if name.endswith("run_manual_tree.py"):
        source = source.replace("завершены по пяти seeds", "завершены по выбранным seeds")
    path.write_text(source, encoding="utf-8")

for name in ["CONTEXT.md", "RelBenchGNN/README.md", "baseline/MANUAL_BASELINE.md"]:
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    text += "\n\n## Изменение плана 2026-10-14: один seed\n\nПо просьбе пользователя для ускорения используются только seed 42: ID-GNN,\nDecisionTree и LightGBM. План задан в RelBenchGNN/experiment_plan.json.\nSeed 42 завершил 20 эпох; начатый seed 43 остановлен, 44–46 исключены.\nАртефакты остановленного запуска сохранены, в сравнении не используются.\nПосле seed 42 выполняются независимый инференс, деревья и графики.\nЭто одиночный локальный результат в сравнении со средним пяти запусков\nстатьи; стандартное отклонение локальных seeds не оценивается.\nПредыдущие описания пяти локальных запусков заменены этим решением.\n"
    path.write_text(text, encoding="utf-8")
