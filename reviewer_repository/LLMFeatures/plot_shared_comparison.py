"""Compare frozen models on identical full test users and ID-GNN pools."""
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from relbench import load_dataset

from features import ROOT

OUT = ROOT / "reports/llmfe_qwen25coder7b_v2/shared_idgnn"
RUN = ROOT / "LLMFeatures/results/qwen25coder7b_seed42_v2/shared_idgnn"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main():
    task = load_dataset(ROOT / "data/rel-hm").load_task("user-item-purchase")
    table = task.get_table("test", mask_input_cols=False).df
    models = {
        "ID-GNN": ROOT / "RelBenchGNN/results/seed_42/test_predictions.npy",
        "LightGBM ручные": ROOT / "baseline/results/manual_v1/lightgbm/seed_42/test_predictions.npy",
        "LightGBM LLM": RUN / "shared_test_predictions.npy",
        "DecisionTree ручные": ROOT / "baseline/results/manual_v1/decision_tree/seed_42/test_predictions.npy"}
    comparison = pd.read_csv(OUT / "comparison.csv")
    aps, ranks, manifest = {}, {}, {}
    for index, (name, path) in enumerate(models.items()):
        predictions = np.load(path)
        if predictions.shape != (len(table), 12):
            raise RuntimeError("Prediction shapes differ")
        hits = np.array([np.isin(pred, true) for pred, true in zip(predictions, table.article_id)])
        denominators = np.minimum(table.article_id.map(len).to_numpy(), 12)
        if (denominators == 0).any():
            raise RuntimeError("Unexpected empty targets; adapt AP filtering")
        ap = (np.cumsum(hits, axis=1)/np.arange(1, 13)*hits).sum(axis=1)/denominators
        expected = comparison.test_map.iloc[index]
        if not np.isclose(ap.mean(), expected, atol=1e-12):
            raise RuntimeError(f"Saved MAP and per-user AP differ: {name}")
        aps[name] = ap
        ranks[name] = np.where(hits.any(axis=1), hits.argmax(axis=1)+1, 0)
        manifest[name] = {"prediction_file": str(path.relative_to(ROOT)),
                          "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                          "test_map": float(ap.mean()), "users_with_hit": int((ranks[name] > 0).sum()),
                          "zero_ap_users": int((ap == 0).sum())}
    pd.DataFrame({"customer_id": table.customer_id.values, **aps}).to_csv(OUT / "test_user_ap.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    ax = axes[0]
    names = list(aps)
    zeros = [100*np.mean(aps[name] == 0) for name in names]
    bars = ax.barh(names, zeros, color=["#4c78a8", "#f28e2b", "#59a14f", "#b07aa1"])
    ax.bar_label(bars, fmt="%.2f%%", padding=3)
    ax.set(xlim=(0, 105), xlabel="Доля test-пользователей, %", title="Ни одного попадания в top-12")
    ax = axes[1]
    bins = np.linspace(0, 100, 21)
    for name, values in aps.items():
        positive = 100*values[values > 0]
        ax.hist(positive, bins=bins, histtype="step", linewidth=1.6, label=name)
    ax.set_yscale("log")
    ax.set(xlabel="AP@12, %", ylabel="Число пользователей (лог. шкала)", title="Распределение AP среди пользователей с попаданиями")
    ax.legend(fontsize=8)
    fig.suptitle("Одинаковые test-пользователи и кандидаты ID-GNN, seed42")
    save(fig, "ap_histograms.png")

    fig, ax = plt.subplots(figsize=(12, 4.8))
    x = np.arange(13)
    for index, (name, values) in enumerate(ranks.items()):
        counts = np.array([np.mean(values == rank) for rank in [*range(1, 13), 0]])*100
        ax.bar(x+(index-1.5)*.2, counts, width=.2, label=name)
    ax.set_xticks(x, [*map(str, range(1, 13)), "Нет"])
    ax.set_yscale("log")
    ax.set(xlabel="Позиция первого релевантного товара", ylabel="Доля пользователей, % (лог. шкала)",
           title="Первое попадание в рекомендациях: полный test")
    ax.legend(fontsize=9)
    save(fig, "first_hit_rank.png")

    delta = aps["LightGBM LLM"]-aps["LightGBM ручные"]
    same = np.isclose(delta, 0, atol=1e-15)
    better = int((delta > 1e-15).sum())
    worse = int((delta < -1e-15).sum())
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.4))
    bars = axes[0].bar(["LLM лучше", "Одинаковый AP", "Ручные лучше"],
                       [better, int(same.sum()), worse], color=["#59a14f", "#bab0ac", "#f28e2b"])
    axes[0].bar_label(bars, padding=3)
    axes[0].set(ylabel="Пользователи", title="Парное сравнение AP@12 на test")
    axes[1].hist(100*delta[~same], bins=np.linspace(-100, 100, 41), color="#4c78a8", edgecolor="white")
    axes[1].axvline(0, color="black", linewidth=1)
    axes[1].set_yscale("log")
    axes[1].set(xlabel="AP LLM − AP ручных, процентные пункты", ylabel="Пользователи (лог. шкала)",
                title="Разница качества; одинаковый AP исключён")
    save(fig, "paired_comparison.png")

    manifest.update(test_users=len(table), paired={"llm_better": better, "equal": int(same.sum()), "manual_better": worse},
                    protocol="identical ID-GNN candidate pools; post-selection test analysis; no model changes")
    (OUT / "plot_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    report = OUT / "report.md"
    content = report.read_text(encoding="utf-8")
    if "ap_histograms.png" not in content:
        content += "\n## Гистограммы и сравнение по пользователям\n\n"
        content += "![Распределение AP и доля нулевых попаданий](ap_histograms.png)\n\n"
        content += "![Позиция первого попадания](first_hit_rank.png)\n\n"
        content += "![Парное сравнение LLM и ручных признаков](paired_comparison.png)\n\n"
        content += "Исходные AP по пользователям: test_user_ap.csv. Средние AP проверены на совпадение с итоговыми MAP.\n"
        report.write_text(content, encoding="utf-8")
    print(json.dumps({"test_users": len(table), "llm_better": better, "same": int(same.sum()), "manual_better": worse}), flush=True)


if __name__ == "__main__":
    main()
