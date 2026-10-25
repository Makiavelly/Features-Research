"""Track already-running processes as well as new instrumented runs."""
import json
from pathlib import Path
import time
import re
import subprocess
import sys

import psutil
from tracking import record
from experiment_plan import selected_seeds
SEEDS = selected_seeds()

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def main():
    record("monitor_start", "Запущено автоматическое обновление истории по процессам и артефактам каждые 30 секунд.")
    last_report_signature = None
    while True:
        state = read_json(ROOT / "experiments/state.json") or {"runs": {}}
        active = set()
        for process in psutil.process_iter(["cmdline"]):
            try:
                command = process.info["cmdline"] or []
                if any("run_idgnn.py" in value for value in command) and "--output_dir" in command:
                    active.add(Path(command[command.index("--output_dir") + 1]).name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        for seed in SEEDS:
            folder = ROOT / f"RelBenchGNN/results/seed_{seed}"
            run_id = f"hm_idgnn_last_seed_{seed}_v1"
            previous = state["runs"].get(run_id, {})
            config = read_json(folder / "config.json")
            if config is None:
                continue
            metrics = read_json(folder / "metrics.json")
            if metrics:
                if previous.get("status") != "complete":
                    record("run_complete", "Полный прогон ID-GNN завершён; метрики прочитаны из итогового файла.", run_id,
                           status="complete", config=config, val_metrics=metrics["val_metrics"],
                           test_metrics=metrics["test_metrics"], epoch=config["epochs"],
                           artifacts=str(folder.relative_to(ROOT)))
                continue
            history = read_json(folder / "history.json")
            if history and history[-1]["epoch"] > previous.get("epoch", 0):
                epoch = history[-1]
                record("epoch", "Завершена эпоха ID-GNN; данные прочитаны из history.json.", run_id,
                       status="training" if folder.name in active else "interrupted_or_pending",
                       config=config, artifacts=str(folder.relative_to(ROOT)), **epoch)
            elif folder.name in active and previous.get("status") not in ["training", "preparing", "preparing_loaders"]:
                log_path = ROOT / f"RelBenchGNN/logs/seed_{seed}.log"
                text = log_path.read_text(errors="replace") if log_path.exists() else ""
                status = "training" if "TRAINING_START" in text else "preparing"
                record("stage", "Полный прогон ID-GNN активен; статус подтверждён процессом и логом.", run_id,
                       status=status, config=config, artifacts=str(folder.relative_to(ROOT)))
            if folder.name in active:
                log_path = ROOT / f"RelBenchGNN/logs/seed_{seed}.log"
                text = log_path.read_text(errors="replace") if log_path.exists() else ""
                if history:
                    marker = f"Epoch: {history[-1]['epoch']:02d},"
                    position = text.rfind(marker)
                    training_text = text[position + len(marker):] if position >= 0 else text
                else:
                    training_text = text
                matches = re.findall(r"\b(\d+)/2000\s*\[", training_text)
                if matches:
                    step = int(matches[-1])
                    current_epoch = history[-1]["epoch"] + 1 if history else 1
                    if step != previous.get("train_step") or current_epoch != previous.get("current_epoch"):
                        record("progress", f"Обучение seed {seed}: эпоха {current_epoch}, шаг {step}/2000.", run_id,
                               status="training", current_epoch=current_epoch, train_step=step,
                               elapsed_note="Эпоха считается завершённой только после записи validation метрики.")
        signature = []
        for seed in SEEDS:
            for filename in ["history.json", "metrics.json", "inference/inference_check.json"]:
                path = ROOT / f"RelBenchGNN/results/seed_{seed}/{filename}"
                signature.append(path.stat().st_mtime_ns if path.exists() else 0)
        signature = tuple(signature)
        manual_signature = []
        for kind in ["decision_tree", "lightgbm"]:
            for seed in SEEDS:
                path = ROOT / f"baseline/results/manual_v1/{kind}/seed_{seed}/metrics.json"
                manual_signature.append(path.stat().st_mtime_ns if path.exists() else 0)
        signature = signature + tuple(manual_signature)
        if signature != last_report_signature:
            with (ROOT / "RelBenchGNN/logs/report.log").open("a") as log:
                report = subprocess.run([sys.executable, str(ROOT / "RelBenchGNN/build_report.py")], stdout=log, stderr=subprocess.STDOUT)
            if report.returncode == 0:
                last_report_signature = signature
            else:
                record("report_error", "Генерация отчёта завершилась ошибкой; проверьте logs/report.log", "hm_visual_report_v1", status="failed")
        exit_path = ROOT / "RelBenchGNN/logs/pipeline.exitcode"
        if exit_path.exists():
            code = exit_path.read_text().strip()
            record("pipeline_exit", f"Конвейер завершился с кодом {code}; статус подтверждён файлом завершения.",
                   "hm_reproduction_pipeline_v1", status="complete" if code == "0" else "failed", exit_code=code)
            if code != "0":
                for seed in SEEDS:
                    folder = ROOT / f"RelBenchGNN/results/seed_{seed}"
                    if (folder / "config.json").exists() and not (folder / "metrics.json").exists():
                        log_path = ROOT / f"RelBenchGNN/logs/seed_{seed}.log"
                        tail = log_path.read_text(errors="replace")[-4000:] if log_path.exists() else ""
                        record("run_failed", "Незавершённый прогон после ошибки конвейера; проверьте лог.",
                               f"hm_idgnn_last_seed_{seed}_v1", status="failed", log_tail=tail)
            break
        pid_path = ROOT / "RelBenchGNN/logs/pipeline.pid"
        if pid_path.exists() and not psutil.pid_exists(int(pid_path.read_text().strip())) and not active:
            record("process_missing", "Процесс конвейера отсутствует, итоговый код не записан; требуется проверка перед возобновлением.",
                   "hm_reproduction_pipeline_v1", status="interrupted")
            break
        time.sleep(30)


if __name__ == "__main__":
    main()
