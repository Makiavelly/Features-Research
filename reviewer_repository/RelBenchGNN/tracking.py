"""Persistent experiment history and cross-session context (run under WSL Python)."""
import argparse
from datetime import datetime
import fcntl
import json
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "experiments"


def atomic_text(path, text):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def render(state):
    runs = state.get("runs", {})
    latest = state["latest_event"]
    lines = ["# Текущий статус", "", f"Обновлено: {latest['time']} (Москва).", "",
             f"Последнее событие: **{latest['message']}**", "",
             "Статус в файле отражает последнее записанное событие. Проверяйте процесс и логи после перерыва.", "",
             "| Запуск | Статус | Завершённые эпохи | Текущая эпоха / шаг | Последнее обновление |", "|---|---|---:|---|---|"]
    for key, run in runs.items():
        progress = f"{run['current_epoch']} / {run.get('train_step', '—')}" if 'current_epoch' in run and run.get('status') == 'training' else '—'
        lines.append(f"| {key} | {run.get('status', run.get('stage', 'unknown'))} | {run.get('epoch', '—')} | {progress} | {run['updated_at']} |")
    lines += ["", "Подробности: [контекст](CONTEXT.md), [результаты](EXPERIMENTS.md), [журнал](WORK_LOG.md).", ""]
    atomic_text(ROOT / "STATUS.md", "\n".join(lines))
    lines = ["# Эксперименты и результаты", "", "MAP@12 указан в процентах. Smoke не является оценкой на полном датасете.", "",
             "Опубликованный RelBench ID-GNN: validation 2.64%, test 2.81% (пять запусков).", "",
             "| Запуск | Статус | Эпоха | Validation MAP, % | Test MAP, % | Артефакты |", "|---|---|---:|---:|---:|---|"]
    for key, run in runs.items():
        val = run.get("val_metrics", {}).get("map")
        test = run.get("test_metrics", {}).get("map")
        val_text = f"{100 * val:.5f}" if val is not None else "—"
        test_text = f"{100 * test:.5f}" if test is not None else "—"
        lines.append(f"| {key} | {run.get('status', 'unknown')} | {run.get('epoch', '—')} | {val_text} | {test_text} | {run.get('artifacts', '—')} |")
    lines += ["", "Текущая конфигурация и ограничения сравнения: [RelBenchGNN/README.md](RelBenchGNN/README.md).", "",
              "Новые протоколы должны получать новые run_id. Завершённые результаты сохраняются в истории.", ""]
    atomic_text(ROOT / "EXPERIMENTS.md", "\n".join(lines))


def record(kind, message, run_id=None, **data):
    DIRECTORY.mkdir(exist_ok=True)
    with (DIRECTORY / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        timestamp = datetime.now(ZoneInfo("Europe/Moscow")).isoformat(timespec="seconds")
        event = {"time": timestamp, "kind": kind, "message": message, "run_id": run_id, "data": data}
        state_file = DIRECTORY / "state.json"
        state = json.loads(state_file.read_text()) if state_file.exists() else {"schema_version": 1, "runs": {}}
        state["latest_event"] = event
        if run_id:
            run = state["runs"].setdefault(run_id, {})
            run.update(data)
            run["updated_at"] = timestamp
            run["last_message"] = message
        with (DIRECTORY / "events.jsonl").open("a", encoding="utf-8") as log:
            log.write(json.dumps(event, ensure_ascii=False) + "\n")
        journal = ROOT / "WORK_LOG.md"
        if not journal.exists():
            journal.write_text("# Журнал работы и экспериментов\n\nИстория добавляется в конец; время московское.\n", encoding="utf-8")
        with journal.open("a", encoding="utf-8") as log:
            log.write(f"\n## {timestamp} — {kind}\n\n{message}\n")
            if run_id:
                log.write(f"\nЗапуск: `{run_id}`.\n")
            if data:
                log.write("\n```json\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n```\n")
        atomic_text(state_file, json.dumps(state, ensure_ascii=False, indent=2) + "\n")
        render(state)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("kind")
    parser.add_argument("message")
    parser.add_argument("--run-id")
    parser.add_argument("--status")
    parser.add_argument("--json-data", default="{}")
    args = parser.parse_args()
    data = json.loads(args.json_data)
    if args.status:
        data["status"] = args.status
    record(args.kind, args.message, args.run_id, **data)


if __name__ == "__main__":
    main()
