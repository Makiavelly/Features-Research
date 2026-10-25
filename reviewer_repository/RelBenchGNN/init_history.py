"""Backfill verified setup/results from this session, without inventing past timestamps."""
import json
from pathlib import Path

from tracking import record

ROOT = Path(__file__).resolve().parents[1]
if (ROOT / "experiments/state.json").exists():
    raise SystemExit("History already initialized; use tracking.py for new events")

record("context", "Добавлен постоянный журнал по просьбе пользователя. Следующие записи фиксируют уже выполненные действия ретроспективно; время — момент записи.")
record("setup", "Скачаны RelBench и экспертные SQL; создано локальное окружение WSL; unsloth и системный драйвер не изменялись.",
       upstream_commit="919fb8a61a4b4cb787283860597f45701895578d", torch="2.2.2+cu118",
       environment="RelBenchGNN/.venv-wsl", checked_unsloth_torch="2.5.1+cu121")
record("compatibility_fix", "Исправлена несовместимость PyArrow 26 с NumPy 1.26: установлен PyArrow 15.0.2 и зафиксированы версии научных библиотек.")
download = json.loads((ROOT / "data/download_manifest.json").read_text())
record("data_download", "Локальный H&M скачан, размеры и SHA256 проверены; проверено чтение всех label-таблиц.",
       "hm_data_snapshot_v1", status="complete", revision=download["revision"],
       files=len(download["files"]), artifacts="data/download_manifest.json")
record("protocol", "Выбрано воспроизведение исходного кода с last; статья указывает uniform. Seeds 42..46 выбраны нами. Оценочный batch уменьшен до 128; обучающий 512 сохранён.",
       published_val_map_percent=2.64, published_test_map_percent=2.81)
baselines = json.loads((ROOT / "baseline/results/simple_metrics.json").read_text())
for name in ["global_popularity", "past_visit"]:
    record("baseline_complete", f"Завершён baseline {name} на полном validation/test", f"hm_{name}_v1",
           status="complete", val_metrics=baselines["val"][name], test_metrics=baselines["test"][name],
           artifacts="baseline/results/simple_metrics.json")
record("discrepancy", "Past-visit MAP отличается от опубликованного результата; причина не установлена, параметры и метрики не подгонялись.")
for seed in range(42, 47):
    record("planned_run", "Запланирован полный прогон ID-GNN", f"hm_idgnn_last_seed_{seed}_v1",
           status="pending", seed=seed, artifacts=f"RelBenchGNN/results/seed_{seed}")
smoke_path = ROOT / "RelBenchGNN/results/smoke/metrics.json"
if smoke_path.exists():
    result = json.loads(smoke_path.read_text())
    record("smoke_complete", "Короткая техническая проверка завершена; метрики не сравниваются со статьёй.",
           "hm_idgnn_smoke_v1", status="smoke_complete", smoke=True,
           val_metrics=result["val_metrics"], test_metrics=result["test_metrics"],
           artifacts="RelBenchGNN/results/smoke")
else:
    record("stage", "Короткая проверка ID-GNN: граф построен, обучение начато; завершение ещё не подтверждено.",
           "hm_idgnn_smoke_v1", status="training", smoke=True, artifacts="RelBenchGNN/results/smoke")
record("stage", "Фоновый конвейер запущен; текущий этап следует сверять с процессом и логами.",
       "hm_reproduction_pipeline_v1", status="running", artifacts="RelBenchGNN/logs")
