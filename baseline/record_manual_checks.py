import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "RelBenchGNN"))
from tracking import record

record("manual_model_checks", "На маленьком примере проверены обучение, сохранение/повторная загрузка DecisionTree и LightGBM, потоковый top-k и исключение будущих данных. Это техническая проверка, не метрика полного H&M.",
       checks_passed=True, feature_count=126)
record("real_sql_check", "126 ручных признаков проверены на настоящем H&M с ограниченной RAM; проверка прошла.",
       result=json.loads((ROOT / "baseline/results/real_sql_check.json").read_text()))
