"""Final report for the frozen small dataset and all requested models."""
import csv
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from relbench import load_dataset
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "RelBenchGNN"))
from tracking import record
BASE = ROOT / "ContextGNN/results/hm_small_v1"
OUT = ROOT / "reports/contextgnn_small_v1"
OUT.mkdir(parents=True, exist_ok=True)
subset = json.loads((ROOT / "data/rel-hm-small-v1/subset_manifest.json").read_text())
task = load_dataset(ROOT / "data/rel-hm-small-v1").load_task("user-item-purchase")
verification = json.loads((BASE / "verification.json").read_text())
assert verification["passed"]
rows, results, quality = [], {}, {}
models = [("idgnn", "ID-GNN"), ("contextgnn", "ContextGNN"),
          ("lightgbm_manual", "LightGBM + manual"), ("lightgbm_idgnn", "LightGBM + ID-GNN features")]
if (BASE / "two_tower/metrics.json").exists():
    models.insert(2, ("two_tower", "Two-tower GraphSAGE"))
for kind, label in models:
    result = json.loads((BASE / kind / "metrics.json").read_text())
    if kind.startswith("lightgbm") or kind=="two_tower":
        assert json.loads((BASE / kind / "verification.json").read_text())["passed"]
    results[kind] = result
    row = {"method": label, "validation_map_percent": 100*result["val_metrics"]["map"],
           "test_map_percent": 100*result["test_metrics"]["map"],
           "training_seconds": result.get("training_and_validation_seconds", result.get("training_and_tuning_seconds")),
           "val_inference_seconds": result["val_inference_seconds"], "test_inference_seconds": result["test_inference_seconds"]}
    rows.append(row)
    per_split = {}
    for split in ["val", "test"]:
        pred = np.load(BASE / kind / f"{split}_predictions.npy")
        target = task.get_table(split, mask_input_cols=False).df
        assert pred.shape == (len(target), 12)
        assert ((pred>=0)&(pred<5000)).all()
        ap = []
        for predicted, true in zip(pred, target.article_id):
            hit = np.isin(predicted, true)
            ap.append(float((np.cumsum(hit)/np.arange(1,13)*hit).sum()/min(len(true),12)))
        assert abs(np.mean(ap)-result[f"{split}_metrics"]["map"]) < 1e-12
        per_split[split] = np.asarray(ap)
        np.save(BASE / kind / f"{split}_ap_per_user.npy", per_split[split])
    quality[kind] = per_split
assert results["lightgbm_manual"]["train_pair_sha256"] == results["lightgbm_idgnn"]["train_pair_sha256"]
tx = pd.read_parquet(ROOT / "data/rel-hm-small-v1/db/transactions.parquet")
pop = {"method": "Popularity", "training_seconds": 0., "val_inference_seconds": 0., "test_inference_seconds": 0.}
for split, cutoff in [("val", "2020-09-07"), ("test", "2020-09-14")]:
    counts = tx[tx.t_dat<=pd.Timestamp(cutoff)].article_id.value_counts().reindex(np.arange(5000), fill_value=0)
    ranking = np.lexsort((np.arange(5000), -counts.values))[:12]
    target = task.get_table(split, mask_input_cols=False)
    pred = np.tile(ranking, (len(target.df),1))
    metric = task.evaluate(pred, target)
    pop["validation_map_percent" if split=="val" else "test_map_percent"] = 100*metric["map"]
rows.insert(0, pop)
with (OUT / "comparison.csv").open("w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[1]))
    writer.writeheader()
    writer.writerows(rows)
fig, axes = plt.subplots(1,2, figsize=(15,4.7), sharey=True)
for axis, split in zip(axes,["validation", "test"]):
    values = [row[f"{split}_map_percent"] for row in rows]
    axis.bar(range(len(rows)), values, color=["#9aa4ae", "#2678b8", "#36a277", "#558a99", "#e4a140", "#9267b0"])
    for index, value in enumerate(values):
        axis.text(index, value+.07, f"{value:.3f}", ha="center", fontsize=9)
    short_labels = {"LightGBM + manual":"LightGBM\nmanual", "LightGBM + ID-GNN features":"LightGBM\nID-GNN features", "Two-tower GraphSAGE":"Two-tower\nGraphSAGE"}
    axis.set_xticks(range(len(rows)), [short_labels.get(row["method"],row["method"]) for row in rows], fontsize=9)
    axis.set_title(split.capitalize())
    axis.set_ylim(0,max(max(row["validation_map_percent"],row["test_map_percent"]) for row in rows)*1.2)
axes[0].set_ylabel("MAP@12 (%)")
fig.suptitle("H&M small pilot — same 5,000-item catalog, seed 42")
fig.tight_layout()
for ext in ["png", "svg"]:
    fig.savefig(OUT / f"comparison.{ext}", dpi=180)
plt.close(fig)
neural_models = [kind for kind in ["idgnn","contextgnn","two_tower"] if kind in results]
fig, axes = plt.subplots(len(neural_models),2, figsize=(11,3.5*len(neural_models)))
for row, kind in enumerate(neural_models):
    history = json.loads((BASE / kind / "history.json").read_text())
    epochs = [value["epoch"] for value in history]
    axes[row,0].plot(epochs, [value["train_loss"] for value in history], marker="o")
    axes[row,0].set_title(kind+" training "+{"idgnn":"BCE","contextgnn":"sparse CE","two_tower":"BPR"}[kind])
    axes[row,1].plot(epochs, [100*value["val_metrics"]["map"] for value in history], marker="o")
    axes[row,1].set_title(kind+" validation MAP@12 (%)")
for axis in axes.flat:
    axis.set_xlabel("Completed epoch")
    axis.set_xticks(range(1,11))
    axis.grid(alpha=.2)
fig.tight_layout()
fig.savefig(OUT / "learning_curves.png", dpi=180)
plt.close(fig)
rng = np.random.default_rng(2026)
diff = quality["contextgnn"]["test"]-quality["idgnn"]["test"]
bootstrap = diff[rng.integers(0,len(diff),size=(2000,len(diff)))].mean(axis=1)*100
interval = np.quantile(bootstrap, [.025,.975]).tolist()
lines = ["# ContextGNN: малый H&M пилот", "", f"Все {len(models)} моделей обучены/пересчитаны и проверены. Seed42, полный каталог поднабора 5,000 товаров.", "",
    "Это изменённая подзадача: 5,000 пользователей, 46,442 транзакции, 8 train времён; train4,804, val304, test250 user-time.",
    "Пользователи/каталог выбраны только по pre-validation истории. После ограничения каталога удалены пустые цели; положительное покрытие val37.27%, test33.68%. MAP не сопоставим напрямую с полным H&M/статьёй.", "",
    "| Модель | Validation MAP, % | Test MAP, % | Обучение + val/tuning, с | Test infer, с |", "|---|---:|---:|---:|---:|"]
for row in rows:
    lines.append(f"| {row['method']} | {row['validation_map_percent']:.5f} | {row['test_map_percent']:.5f} | {row['training_seconds']:.2f} | {row['test_inference_seconds']:.3f} |")
lines += ["", "Время inference в таблице измерено после подготовки графа/модели и GPU warm-up, не включает импорт библиотек. Первый независимый вызов может включать существенную GPU инициализацию; timings сохранены в verification.json.", "",
    "![Сравнение](comparison.png)", "", "![Кривые](learning_curves.png)", "",
    "## Сопоставимость и ограничения", "",
    "Оба LightGBM обучены на одних 72,813 парах (все позитивы + до8history/8uniform negatives). SHA отсортированных ключей/меток совпадает. 126 ручных признаков заново рассчитаны на малом графе. ID-GNN features:64 замороженных координаты перед головой + availability; train representations in-sample, не OOF.",
    "Оценочные файлы обоих LightGBM проверены на точное равенство user×catalog:304×5000 val,250×5000 test. Все модели оцениваются на этих же пользователях и каталоге. ID-GNN присваивает ноль вне локального подграфа; ContextGNN использует глобальные scores.",
    "Нейросети имеют разные objectives (BCE, sparse CE, BPR для двухбашенной), а LightGBM другой бюджет/negative sampling. Сравнение характеризует конвейеры, не изолированный эффект архитектуры. Выбор checkpoints/параметров только по validation; test не использован для подбора.",
    f"Разница test ContextGNN−ID-GNN {diff.mean()*100:.4f} п.п.; парный bootstrap95% по test пользователям [{interval[0]:.4f}; {interval[1]:.4f}] п.п. Это условный интервал по250пользователям, не оценка вариативности обучения по seeds.", "",
    "## Доступность ID-GNN представлений", "", "| Split | Пар | Без локального вектора | Доля |", "|---|---:|---:|---:|"]
for split, counts in results["lightgbm_idgnn"]["embedding_coverage"].items():
    lines.append(f"| {split} | {counts['pairs']} | {counts['missing_embeddings']} | {counts['missing_embeddings']/counts['pairs']:.2%} |")
lines += ["", "Отсутствующие локальные векторы заполнены нулями и availability=0. На полном каталоге таких пар существенно больше, чем в прежнем локальном reranking experiment. Это ограничивает LightGBM на ID-GNN признаках и не является свидетельством бесполезности GNN-признаков вообще.", "",
    "Официальный ContextGNN commit ca4a96985b7ef73c36a40da32e70710ad9b59a1e. Обёртка очищает RHS FUSION cache перед eval, чтобы не использовать прошлую версию матрицы; upstream неизменён.",
    "В статье для полного H&M ContextGNN val3.00%,test2.93%: приведено только как отдельный результат, не цель/сравнение чисел этого поднабора.",
    "[Протокол](../../ContextGNN/PROTOCOL_SMALL.md) · [Манифест](../../data/rel-hm-small-v1/subset_manifest.json)", ""]
if "two_tower" in results:
    lines += ["## Добавление двухбашенной архитектуры", "",
        "Используется Model из RelBenchGNN/upstream/examples/model.py, как в прежнем большом двухбашенном запуске. Пользователь и товар кодируются отдельными forward с общими параметрами; скор — dot product. Глобальные user/item представления доступны для всех пар малого каталога.",
        "Размеры согласованы с малым пилотом: 64канала,2GNNслоя,ResNet encoder64×2,neighbors32/16,batch128,last sampling,до10эпох,patience3. BPR с same-time in-batch negatives. Неполные timestamp batches сохранены: каждая эпоха содержит все4804train строки.",
        "Прежние четыре модели не переобучались. Предыдущая версия отчёта сохранена в before_two_tower/. Новый run_id hm_twotower_small_seed_42_v1, независимый replay best.pt проверен.", ""]
(OUT / "report.md").write_text("\n".join(lines), encoding="utf-8")
(OUT / "report.json").write_text(json.dumps({"final": True, "comparison": rows, "subset": subset, "results": results,
    "gnn_verification": verification,
    "two_tower_verification": json.loads((BASE / "two_tower/verification.json").read_text()) if "two_tower" in results else None,
    "context_minus_idgnn_test_bootstrap95_pp": interval}, indent=2))
record("small_pilot_complete", f"Малый пилот завершён: {len(models)} моделей оценены по всем5000товарам; модели проверены, MAP пересчитан из сохранённых предсказаний, общие пары/кандидаты сверены. Отчёт и графики сохранены отдельно от полного H&M.", "hm_contextgnn_small_pipeline_v1", status="complete", comparison=rows, artifacts=str(OUT.relative_to(ROOT)))
print(json.dumps(rows, indent=2), flush=True)
