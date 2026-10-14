"""Export measured results as CSV, Markdown, PNG and SVG, without running models."""
import csv
from datetime import datetime
import json
import fcntl
from pathlib import Path
import statistics
from zoneinfo import ZoneInfo

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from tracking import record
from experiment_plan import selected_seeds
SEEDS = selected_seeds()

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/relbench_hm_v1"


def load(path):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def export_csv(name, rows):
    temporary = OUT / (name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(OUT / name)


def save_plot(fig, name):
    for extension in ["png", "svg"]:
        temporary = OUT / f"{name}.tmp.{extension}"
        fig.savefig(temporary, dpi=180, bbox_inches="tight")
        temporary.replace(OUT / f"{name}.{extension}")
    plt.close(fig)


def fmt(value):
    return f"{value:.5f}" if value is not None else "—"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.grid": True, "grid.alpha": 0.18, "axes.axisbelow": True})
    seeds, histories, finished, verified = [], {}, [], []
    for seed in SEEDS:
        folder = ROOT / f"RelBenchGNN/results/seed_{seed}"
        history = load(folder / "history.json") or []
        metrics = load(folder / "metrics.json")
        check = load(folder / "inference/inference_check.json")
        histories[seed] = history
        if metrics:
            finished.append(metrics)
        if check and check.get("passed"):
            verified.append(seed)
        seeds.append({"seed": seed, "completed_epochs": len(history),
                      "best_validation_so_far_percent": max((100 * r["val_metrics"]["map"] for r in history), default=None),
                      "final_validation_percent": 100 * metrics["val_metrics"]["map"] if metrics else None,
                      "final_test_percent": 100 * metrics["test_metrics"]["map"] if metrics else None,
                      "inference_verified": check["passed"] if check else None,
                      "test_inference_seconds": check["test_inference_seconds"] if check else None,
                      "test_users_per_second": check["test_users_per_second"] if check else None})
    export_csv("seeds.csv", seeds)
    baseline = load(ROOT / "baseline/results/simple_metrics.json")
    rows = []
    for name, label, paper_val, paper_test in [("global_popularity", "Global popularity", 0.36, 0.30), ("past_visit", "Past visit", 1.07, 0.89)]:
        val = baseline["val"][name]["map"] * 100 if baseline else None
        test = baseline["test"][name]["map"] * 100 if baseline else None
        rows.append({"method": label, "validation_map_percent": val, "test_map_percent": test,
                     "published_validation_percent": paper_val, "published_test_percent": paper_test,
                     "test_difference_pp": test - paper_test if test is not None else None})
    val_values = [100 * run["val_metrics"]["map"] for run in finished]
    test_values = [100 * run["test_metrics"]["map"] for run in finished]
    val_mean = statistics.mean(val_values) if val_values else None
    test_mean = statistics.mean(test_values) if test_values else None
    rows.append({"method": f"ID-GNN ({len(finished)}/{len(SEEDS)} completed)", "validation_map_percent": val_mean,
                 "test_map_percent": test_mean, "published_validation_percent": 2.64,
                 "published_test_percent": 2.81, "test_difference_pp": test_mean - 2.81 if test_mean is not None else None})
    manual_runs = {}
    spreads = [None, None, statistics.pstdev(test_values) if len(test_values) > 1 else None]
    for kind, label in [("decision_tree", "DecisionTree + manual"), ("lightgbm", "LightGBM + manual")]:
        records = []
        for seed in SEEDS:
            result = load(ROOT / f"baseline/results/manual_v1/{kind}/seed_{seed}/metrics.json")
            if result:
                records.append(result)
        manual_runs[kind] = records
        vals = [100 * r["val_metrics"]["map"] for r in records]
        tests = [100 * r["test_metrics"]["map"] for r in records]
        rows.append({"method": f"{label} ({len(records)}/{len(SEEDS)} completed)",
                     "validation_map_percent": statistics.mean(vals) if vals else None,
                     "test_map_percent": statistics.mean(tests) if tests else None,
                     "published_validation_percent": None, "published_test_percent": None, "test_difference_pp": None})
        spreads.append(statistics.pstdev(tests) if len(tests) > 1 else None)
    export_csv("comparison.csv", rows)
    complete = len(finished) == len(SEEDS) and len(verified) == len(SEEDS) and all(len(records) == len(SEEDS) for records in manual_runs.values())
    timestamp = datetime.now(ZoneInfo("Europe/Moscow")).isoformat(timespec="seconds")
    metadata = {"updated_at": timestamp, "final": complete, "selected_seeds": SEEDS, "expected_runs": len(SEEDS), "completed_training_runs": len(finished),
                "verified_inference_seeds": verified, "comparison": rows, "seeds": seeds,
                "validation_std_percent": statistics.pstdev(val_values) if len(val_values) > 1 else None,
                "test_std_percent": statistics.pstdev(test_values) if len(test_values) > 1 else None,
                "published_validation_std_percent": 0.00, "published_test_std_percent": 0.01}
    metadata["manual_baselines"] = {kind: {"completed_runs": len(records),
        "val_std_percent": statistics.pstdev([100*r["val_metrics"]["map"] for r in records]) if len(records) > 1 else None,
        "test_std_percent": statistics.pstdev([100*r["test_metrics"]["map"] for r in records]) if len(records) > 1 else None} for kind, records in manual_runs.items()}
    (OUT / "report.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8), sharey=True)
    for ax, split, paper_key in [(axes[0], "validation", "published_validation_percent"), (axes[1], "test", "published_test_percent")]:
        for index, row in enumerate(rows):
            if row[paper_key] is not None:
                ax.bar(index + .18, row[paper_key], width=.34, color="#bbc3cc")
        for i, row in enumerate(rows):
            value = row[f"{split}_map_percent"]
            if value is not None:
                if i == 2:
                    spread = statistics.pstdev(val_values if split == "validation" else test_values) if len(finished) > 1 else None
                elif i >= 3:
                    kind = ["decision_tree", "lightgbm"][i-3]
                    spread = metadata["manual_baselines"][kind]["val_std_percent" if split == "validation" else "test_std_percent"]
                else:
                    spread = None
                ax.bar(i - .18, value, width=.34, color="#2678b8", yerr=spread, capsize=3)
                ax.text(i - .18, value + .05, f"{value:.3f}", ha="center", fontsize=8)
            else:
                ax.text(i - .18, .06, "pending", rotation=90, ha="center", fontsize=9)
        ax.set_xticks(np.arange(len(rows)), ["Popularity", "Past visit", "ID-GNN", "DecisionTree\nmanual", "LightGBM\nmanual"], fontsize=9)
        ax.set_xlabel("Methods on the same H&M purchase task")
        ax.set_xlim(-.6, len(rows)-.4)
        ax.set_title(split.capitalize())
        ax.set_ylim(0, max(3.2, max((r[f"{split}_map_percent"] or 0 for r in rows)) * 1.15))
    axes[0].set_ylabel("MAP@12 (%)")
    fig.suptitle(f"RelBench H&M — {'final verified report' if complete else 'partial results'}")
    fig.legend(handles=[Patch(color="#2678b8", label="Our complete runs"), Patch(color="#bbc3cc", label="Published RelBench")], loc="lower center", ncol=2, bbox_to_anchor=(.5, 0))
    fig.tight_layout(rect=(0, .13, 1, 1))
    save_plot(fig, "comparison")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
    for seed, history in histories.items():
        if history:
            epochs = [r["epoch"] for r in history]
            axes[0].plot(epochs, [100 * r["val_metrics"]["map"] for r in history], marker="o", markersize=3, label=f"seed {seed}")
            axes[1].plot(epochs, [r["train_loss"] for r in history], marker="o", markersize=3, label=f"seed {seed}")
    axes[0].axhline(2.64, color="#6c737a", linestyle="--", label="Published validation MAP")
    axes[0].set_ylabel("Validation MAP@12 (%)")
    axes[1].set_ylabel("Training BCE loss")
    for ax in axes:
        ax.set_xlabel("Completed epoch")
        ax.set_xlim(.5, 20.5)
        ax.set_xticks([1, 5, 10, 15, 20])
        ax.legend(fontsize=8)
    fig.suptitle("Learning curves — full validation, each seed separately")
    fig.tight_layout()
    save_plot(fig, "learning_curves")
    if verified:
        fig, ax = plt.subplots(figsize=(8, 4.5))
        bins, histogram_rows = np.linspace(0, 1, 21), []
        for seed in verified:
            ap = np.load(ROOT / f"RelBenchGNN/results/seed_{seed}/inference/test_ap_per_user.npy")
            ax.hist(ap, bins=bins, histtype="step", linewidth=1.6, label=f"seed {seed}")
            counts, _ = np.histogram(ap, bins=bins)
            histogram_rows.extend({"seed": seed, "ap_left": left, "ap_right": right, "users": int(count)} for left, right, count in zip(bins[:-1], bins[1:], counts))
        ax.set_yscale("log")
        ax.set_xlabel("Per-user AP@12 (fraction)")
        ax.set_ylabel("Number of users (log scale)")
        ax.set_title("Verified test inference: recommendation quality distribution")
        ax.legend()
        save_plot(fig, "test_ap_distribution")
        export_csv("test_ap_distribution.csv", histogram_rows)
    lines = ["# RelBench H&M: результаты воспроизведения", "", f"Обновлено: {timestamp} (Москва).", "",
             "**Финальный отчёт: GNN, инференс и обе модели на ручных признаках завершены.**" if complete else "**Промежуточный отчёт: обучение, инференс и/или ручные baseline ещё не завершены.**", "",
             f"Завершено обучение: {len(finished)}/{len(SEEDS)}. Проверено независимым инференсом: {len(verified)}/{len(SEEDS)}.", "",
             "MAP@12 указан в процентах. Локальный эксперимент использует один seed 42 по просьбе пользователя. Статья сообщает среднее пяти запусков; локальный разброс по seeds не оценён.", "",
             "Источник опубликованных значений: [RelBench, таблица 8](https://arxiv.org/html/2407.20060v1). Усы на столбцах ID-GNN показывают стандартное отклонение между завершёнными seeds.", "",
             "| Метод | Validation MAP, % | Test MAP, % | Test в статье, % | Разница, п.п. |", "|---|---:|---:|---:|---:|"]
    for r in rows:
        lines.append(f"| {r['method']} | {fmt(r['validation_map_percent'])} | {fmt(r['test_map_percent'])} | {fmt(r['published_test_percent'])} | {fmt(r['test_difference_pp'])} |")
    lines += ["", "Все столбцы по оси X — методы на одной задаче H&M user-item-purchase, а не разные задачи.", "",
              "## Справочные результаты статьи", "",
              "| Метод в статье | Validation MAP, % | Test MAP, % |", "|---|---:|---:|",
              "| Popularity | 0.36 | 0.30 |", "| Past visit | 1.07 | 0.89 |",
              "| LightGBM: сырые признаки + история/популярность | 0.44 | 0.38 |",
              "| RDL GraphSAGE | 0.92 | 0.80 |", "| RDL ID-GNN | 2.64 | 2.81 |", "",
              "Наши DecisionTree/LightGBM manual — отдельные локальные baseline с 126 вручную заданными признаками.",
              "Это адаптированное подмножество экспертных user-churn/item-sales SQL плюс наши признаки пары; авторы не публиковали этот набор для ранжирования.",
              "Опубликованные 0.38% LightGBM относятся к другому набору входов, не к нашей адаптации.",
              "Для основных сравнений каждая модель дерева использует тот же evaluation pool, что и соответствующий seed ID-GNN.",
              "Деревья обучаются на 50,000 user-time строках train; ID-GNN имеет больший supervised бюджет. Test полный; tuning деревьев на 10,000 validation пользователей.",
              "[Протокол ручных признаков](../../baseline/MANUAL_BASELINE.md)", ""]
    lines += ["", "![Сравнение метрик](comparison.png)", "", "![Кривые обучения](learning_curves.png)", "",
              "## Запуски и независимый инференс", "", "| Seed | Эпохи | Лучший validation пока, % | Финальный test, % | Инференс |", "|---|---:|---:|---:|---|"]
    for r in seeds:
        check = "пройден" if r["inference_verified"] is True else "ошибка" if r["inference_verified"] is False else "ожидает обучения"
        lines.append(f"| {r['seed']} | {r['completed_epochs']} | {fmt(r['best_validation_so_far_percent'])} | {fmt(r['final_test_percent'])} | {check} |")
    lines += ["", "## Локальные модели на ручных признаках", "",
              "| Модель | Seed | Validation MAP, % | Test MAP, % | Инференс из сохранённой модели |",
              "|---|---:|---:|---:|---|"]
    for kind, records in manual_runs.items():
        by_seed = {r["seed"]: r for r in records}
        for seed in SEEDS:
            result = by_seed.get(seed)
            val_text = fmt(100 * result["val_metrics"]["map"]) if result else "—"
            test_text = fmt(100 * result["test_metrics"]["map"]) if result else "—"
            lines.append(f"| {kind} | {seed} | {val_text} | {test_text} | {'проверен' if result else 'ожидается'} |")
    if len(val_values) > 1:
        lines += ["", f"Стандартное отклонение между завершёнными seeds: validation {metadata['validation_std_percent']:.5f} п.п., test {metadata['test_std_percent']:.5f} п.п."]
    if verified:
        lines += ["", "![Распределение AP@12](test_ap_distribution.png)"]
    lines += ["", "В новом процессе best.pt загружается строго, затем повторяется полный validation/test.",
              "Проверяются конечность оценок, размеры предсказаний, диапазон и уникальность ID, совпадение MAP с сохранённым результатом (допуск 1e-6 в долях).",
              "Побитовое совпадение записывается отдельно: CUDA может давать небольшие численные различия.", "",
              "Таблицы: [comparison.csv](comparison.csv), [seeds.csv](seeds.csv). Графики также доступны как SVG.", "",
              "Протокол: last соответствует исходному коду, статья указывает uniform; seed 42 выбран нами; число запусков сокращено пользователем до одного; оценочный batch 128 вместо 512.",
              "Past visit отличается от статьи; причина пока не установлена. Smoke-метрики сюда не включены.", "",
              "[Протокол](../../RelBenchGNN/README.md) · [Контекст](../../CONTEXT.md) · [История](../../WORK_LOG.md)", ""]
    temporary = OUT / "report.md.tmp"
    temporary.write_text("\n".join(lines), encoding="utf-8")
    temporary.replace(OUT / "report.md")
    record("report_updated", "Обновлены таблицы и графики результатов", "hm_visual_report_v1", status="complete" if complete else "partial",
           completed_runs=len(finished), verified_inference_runs=len(verified), artifacts="reports/relbench_hm_v1/report.md")
    print(OUT / "report.md", flush=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / ".report.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        main()
