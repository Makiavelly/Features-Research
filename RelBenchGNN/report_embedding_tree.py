"""Standalone report for GNN → LightGBM, preserving the preceding report."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tracking import record

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/gnn_embeddings_v1"
OUT.mkdir(parents=True, exist_ok=True)
rows = []
for title, path in [
    ("ID-GNN", "RelBenchGNN/results/seed_42/metrics.json"),
    ("DecisionTree manual", "baseline/results/manual_v1/decision_tree/seed_42/metrics.json"),
    ("LightGBM manual", "baseline/results/manual_v1/lightgbm/seed_42/metrics.json"),
    ("ID-GNN embeddings + LightGBM", "baseline/results/gnn_embeddings_v1/metrics.json")]:
    result = json.loads((ROOT / path).read_text())
    rows.append({"method": title, "validation_map_percent": 100 * result["val_metrics"]["map"], "test_map_percent": 100 * result["test_metrics"]["map"]})
with (OUT / "comparison.csv").open("w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
for axis, split in zip(axes, ["validation", "test"]):
    vals = [row[f"{split}_map_percent"] for row in rows]
    axis.bar(range(4), vals, color=["#2678b8", "#8899aa", "#8899aa", "#36a277"])
    for index, value in enumerate(vals):
        axis.text(index, value + .04, f"{value:.3f}", ha="center")
    axis.set_xticks(range(4), ["ID-GNN", "Tree\nmanual", "LightGBM\nmanual", "GNN embeddings\n+ LightGBM"], fontsize=9)
    axis.set_title(split.capitalize())
    axis.set_ylim(0, max(vals) * 1.18)
axes[0].set_ylabel("MAP@12 (%)")
fig.suptitle("H&M purchase ranking — seed 42")
fig.tight_layout()
for extension in ["png", "svg"]:
    fig.savefig(OUT / f"comparison.{extension}", dpi=180)
plt.close(fig)
new = json.loads((ROOT / "baseline/results/gnn_embeddings_v1/metrics.json").read_text())
lines = ["# ID-GNN → LightGBM: H&M ranking", "", "Эксперимент завершён, seed 42. Все значения MAP@12 в процентах.", "",
         "| Модель | Validation | Test |", "|---|---:|---:|"]
lines += [f"| {r['method']} | {r['validation_map_percent']:.5f} | {r['test_map_percent']:.5f} |" for r in rows]
lines += ["", "![Сравнение](comparison.png)", "", "Это адаптация RelBench Appendix C.2 к ранжированию: авторы проверяли GNN+LightGBM на регрессии и классификации, опубликованного H&M ranking результата для этой связки нет.",
          "[Статья, приложение C.2](https://arxiv.org/html/2407.20060v1)", "",
          "GNN заморожена: best.pt seed 42, эпоха 19. Извлечены 128 чисел перед линейной головой; её логит не входит в признаки дерева.",
          "Дополнительный gnn_available указывает, существует ли представление пары в подграфе. Для отсутствующих представлений используется нулевой вектор. Итого 129 входов LightGBM.",
          "Использованы те же 50,000 user-time строк и 803,377 обучающих пар, что для ручного baseline. Кандидаты validation/test совпадают с предыдущим ID-GNN; предсказания исходной головы при экспорте проверены на полное совпадение.",
          "GNN ранее обучалась на train, поэтому эмбеддинги для train являются in-sample, без out-of-fold обучения. Бюджет включает предыдущее обучение GNN; сравнение с ручным baseline не уравнивает суммарные затраты.",
          "Параметры дерева выбраны на тех же 10,000 validation пользователях: num_leaves 15/31, 150 итераций. Test не участвовал в выборе. Итоговый инференс выполнен после загрузки сохранённого model.txt.",
          "Опубликованный ID-GNN: validation 2.64%, test 2.81% по пяти запускам. Наши результаты — один seed.", "", "## Доступность представлений", "",
          "| Split | Пар | Без представления |", "|---|---:|---:|"]
lines += [f"| {split} | {value['pairs']} | {value['missing_embeddings']} |" for split, value in new["embedding_counts"].items()]
lines += ["", "## Конфигурация и результаты", "", "```json", json.dumps(new, indent=2, ensure_ascii=False), "```", ""]
(OUT / "report.md").write_text("\n".join(lines), encoding="utf-8")
(OUT / "report.json").write_text(json.dumps({"final": True, "comparison": rows, "experiment": new}, indent=2))
record("embedding_report", "Отчёт GNN → LightGBM сохранён отдельно; предыдущие результаты не заменены", "hm_gnn_embedding_report_v1", status="complete", artifacts=str(OUT.relative_to(ROOT)))
