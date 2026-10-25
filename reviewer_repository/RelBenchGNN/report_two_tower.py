"""Render two-tower progress/results separately from previous experiments."""
import json
import csv
import fcntl
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tracking import record

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/two_tower_v1"
OUT.mkdir(parents=True, exist_ok=True)
report_lock = (OUT / ".report.lock").open("a")
fcntl.flock(report_lock, fcntl.LOCK_EX)
folder = ROOT / "RelBenchGNN/results/two_tower_seed_42"
history = json.loads((folder / "history.json").read_text()) if (folder / "history.json").exists() else []
result = json.loads((folder / "metrics.json").read_text()) if (folder / "metrics.json").exists() else None
check = json.loads((folder / "inference/inference_check.json").read_text()) if (folder / "inference/inference_check.json").exists() else None
rows = []
for name, path in [("ID-GNN", "RelBenchGNN/results/seed_42/metrics.json"),
                   ("LightGBM manual", "baseline/results/manual_v1/lightgbm/seed_42/metrics.json"),
                   ("ID-GNN + LightGBM", "baseline/results/gnn_embeddings_v1/metrics.json")]:
    item = json.loads((ROOT / path).read_text())
    rows.append({"method": name, "validation_map_percent": item["val_metrics"]["map"]*100, "test_map_percent": item["test_metrics"]["map"]*100})
rows.append({"method": "Two-tower GraphSAGE", "validation_map_percent": result["val_metrics"]["map"]*100 if result else None, "test_map_percent": result["test_metrics"]["map"]*100 if result else None})
with (OUT / "comparison.csv").open("w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for axis, split in zip(axes, ["validation", "test"]):
    for index, row in enumerate(rows):
        value = row[f"{split}_map_percent"]
        if value is None:
            axis.text(index, .1, "pending", ha="center")
        else:
            axis.bar(index, value)
            axis.text(index, value+.05, f"{value:.3f}", ha="center")
    axis.set_xticks(range(4), ["ID-GNN", "LightGBM\nmanual", "ID-GNN\n+ LightGBM", "Two-tower\nGraphSAGE"])
    axis.set_ylim(0, 3.4)
    axis.set_title(split)
axes[0].set_ylabel("MAP@12 (%)")
fig.tight_layout()
fig.savefig(OUT / "comparison.png", dpi=180)
plt.close(fig)
if history:
    epochs = [row["epoch"] for row in history]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].plot(epochs, [row["train_loss"] for row in history], marker="o", markersize=4)
    axes[0].set_ylabel("Mean training BPR loss")
    axes[0].set_title("Training loss")
    axes[1].plot(epochs, [100 * row["val_metrics"]["map"] for row in history], marker="o", markersize=4)
    axes[1].axhline(.92, color="gray", linestyle="--", label="Published GraphSAGE validation")
    axes[1].set_ylabel("Validation MAP@12 (%)")
    axes[1].set_title("Full validation quality")
    axes[1].legend(fontsize=8)
    for axis in axes:
        axis.set_xlabel("Completed epoch")
        axis.set_xlim(.5, 20.5)
        axis.set_xticks([1, 5, 10, 15, 20])
        axis.grid(alpha=.25)
    fig.suptitle("Two-tower GraphSAGE — seed 42")
    fig.tight_layout()
    for extension in ["png", "svg"]:
        fig.savefig(OUT / f"learning_curves.{extension}", dpi=180)
    plt.close(fig)
    with (OUT / "learning_curves.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["epoch", "train_bpr_loss", "validation_map_percent"])
        writer.writeheader()
        writer.writerows({"epoch": row["epoch"], "train_bpr_loss": row["train_loss"],
                         "validation_map_percent": 100*row["val_metrics"]["map"]} for row in history)
final = bool(result and check and check.get("passed"))
lines = ["# Двухбашенная GraphSAGE: H&M", "", f"Эпох завершено: {len(history)}/20. Финальный проверенный результат: {final}.", "",
         "| Метод | Validation MAP, % | Test MAP, % |", "|---|---:|---:|"]
for row in rows:
    val = f"{row['validation_map_percent']:.5f}" if row['validation_map_percent'] is not None else "ожидается"
    test = f"{row['test_map_percent']:.5f}" if row['test_map_percent'] is not None else "ожидается"
    lines.append(f"| {row['method']} | {val} | {test} |")
lines += ["", "![Сравнение](comparison.png)", "", "![Loss и validation MAP](learning_curves.png)", "",
          "Графики показывают только завершённые эпохи: средний тренировочный BPR loss и полный validation MAP@12. Обновляются после каждой эпохи; численные значения доступны в learning_curves.csv.", "", "Пользователь и каждый товар кодируются отдельными forward с общими весами GraphSAGE, без ID-awareness. Скор пары — скалярное произведение 128-мерных представлений. BPR loss, shallow embedding товара включён, как в исходном примере.",
          "Оценка двухбашенной модели охватывает весь каталог 105,542 товаров. Предыдущие ID-GNN/manual эксперименты используют локальные кандидаты; это сравнение итоговых конвейеров, не изолированная замена головы при одинаковых кандидатах.",
          "Статья RelBench RDL GraphSAGE: validation 0.92%, test 0.80% MAP@12. Это опубликованная двухбашенная архитектура; наш один seed сравнивается со средним пяти запусков.",
          "[Статья](https://arxiv.org/html/2407.20060v1)",
          "Отклонения от стандартного примера: train batch 256 вместо 512 для памяти GPU; строго 2000 шагов вместо исходного условия на 2001; фиксированное RNG-состояние для каждого evaluation split. Temporal sampling uniform в обучении и оценке.",
          "Все пользовательские и товарные val/test эмбеддинги сохраняются вместе с ID и временем; исходный каталог покрыт полностью. После обучения проверяется инференс best.pt в новом процессе.", ""]
(OUT / "report.md").write_text("\n".join(lines), encoding="utf-8")
(OUT / "report.json").write_text(json.dumps({"final": final, "history": history, "comparison": rows, "inference": check}, indent=2))
record("two_tower_report", "Обновлён отдельный отчёт двухбашенной модели", "hm_twotower_report_v1", status="complete" if final else "partial", artifacts=str(OUT.relative_to(ROOT)))
