"""Read-only visualizations of saved search results; no training/test feedback."""
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import lightgbm as lgb
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "LLMFeatures/results/qwen25coder7b_seed42_v2"
OUT = ROOT / "reports/llmfe_qwen25coder7b_v2/progress"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    state = json.loads((RUN / "search_state.json").read_text())
    trials = state["trials"]
    valid = [trial for trial in trials if trial["status"] == "valid"]
    control = json.loads((RUN / "raw_control/search_metrics.json").read_text())["val_metrics"]["map"]
    confirmation = json.loads((RUN / "confirmation.json").read_text()) if (RUN / "confirmation.json").exists() else []
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.3))
    ax = axes[0]
    if valid:
        x = np.array([trial["candidate"] for trial in valid])
        y = 100*np.array([trial["score"] for trial in valid])
        ax.scatter(x, y, label="Валидный набор", zorder=3)
        ax.step(x, np.maximum.accumulate(y), where="post", label="Лучший найденный MAP")
    ax.axhline(100*control, linestyle="--", color="gray", label="Сырые поля, контроль")
    rejected = [trial["candidate"] for trial in trials if trial["status"] != "valid"]
    ax.scatter(rejected, np.zeros(len(rejected)), marker="x", color="red", label="Отклонено, MAP не измерялся")
    ax.set(xlabel="Номер предложения LLM", ylabel="Search MAP@12, %", title="Поиск: 256 validation-пользователей")
    ax.set_xticks(np.arange(1, 21, 2))
    ax.legend(fontsize=8)
    ax.grid(alpha=.2)
    ax = axes[1]
    if confirmation:
        names = [Path(item["directory"]).name.replace("candidate_", "Набор ") for item in confirmation]
        scores = [100*item["score"] for item in confirmation]
        bars = ax.bar(names, scores, color="#4c78a8")
        ax.bar_label(bars, fmt="%.4f", padding=3)
        ax.set_ylim(0, max(scores)*1.3 if max(scores) > 0 else 1)
    ax.set(ylabel="Confirmation MAP@12, %", title="Подтверждение: другие 1024 пользователя")
    fig.suptitle("LLM-FE v2: промежуточные validation-результаты, не полный test", fontsize=12)
    save(fig, "search_progress.png")

    fig, ax = plt.subplots(figsize=(7, 4))
    islands = np.arange(3)
    good = [sum(t["status"] == "valid" and t["island"] == i for t in trials) for i in islands]
    bad = [sum(t["status"] != "valid" and t["island"] == i for t in trials) for i in islands]
    bars = ax.bar(islands, good, label="Успешно оценены", color="#59a14f")
    ax.bar_label(bars, label_type="center")
    bars = ax.bar(islands, bad, bottom=good, label="Отклонены", color="#e15759")
    ax.bar_label(bars, label_type="center")
    ax.set(xticks=islands, xticklabels=["Популяция A", "Популяция B", "Популяция C"],
           ylabel="Число предложений", title=f"Результаты {len(trials)} попыток LLM")
    ax.legend()
    save(fig, "attempts_histogram.png")

    selected_path = RUN / "selected.json"
    metadata = {"final": False, "completed_proposals": len(trials), "valid": len(valid),
                "rejected": len(trials)-len(valid), "search_users": 256, "confirmation_users": 1024,
                "note": "Only saved validation results; no full-test metrics or training-loss history"}
    catalog_paused = (RUN / "full_catalog_paused.json").exists()
    metadata["full_catalog_paused"] = catalog_paused
    if selected_path.exists():
        selection = json.loads(selected_path.read_text())
        folder = Path(selection["directory"])
        model = lgb.Booster(model_file=str(folder / "model.txt"))
        importance = pd.DataFrame({"feature": model.feature_name(), "gain": model.feature_importance("gain")})
        importance.to_csv(OUT / "feature_importance.csv", index=False)
        importance = importance.sort_values("gain").tail(20)
        fig, ax = plt.subplots(figsize=(10, 7))
        colors = ["#4c78a8" if name.startswith("f_") else "#bab0ac" for name in importance.feature]
        ax.barh(importance.feature, importance.gain, color=colors)
        ax.set(xlabel="LightGBM split gain (не причинный эффект)",
               title=f"Важность признаков: {folder.name}\nСиний — признаки LLM, серый — сырые поля")
        save(fig, "feature_importance.png")

        sys.path.insert(0, str(ROOT / "RelBenchGNN/upstream"))
        from relbench import load_dataset
        task = load_dataset(ROOT / "data/rel-hm").load_task("user-item-purchase")
        indices = np.load(RUN / "validation_selection.npz")["confirm"]
        target = task.get_table("val").df.iloc[indices]
        predictions = np.load(folder / "confirm_val_predictions.npy")
        if len(predictions) != len(target):
            raise RuntimeError("Saved confirmation predictions do not match selection")
        aps = []
        for pred, truth in zip(predictions, target.article_id):
            if not len(truth):
                continue
            hits = np.isin(pred, truth)
            aps.append(float(np.sum(np.cumsum(hits)/(np.arange(12)+1)*hits)/min(len(truth), 12)))
        aps = np.array(aps)
        if not np.isclose(aps.mean(), selection["confirmation_score"], atol=1e-12):
            raise RuntimeError("Per-user AP does not reproduce saved confirmation MAP")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(100*aps, bins=np.linspace(0, 100, 21), color="#4c78a8", edgecolor="white")
        ax.set_yscale("log")
        ax.set(xlabel="AP@12 пользователя, %", ylabel="Пользователи (логарифмическая шкала)",
               title=f"Распределение качества на confirmation validation\n{len(aps)} пользователей; нулевой AP у {(aps == 0).sum()}")
        save(fig, "ap_histogram.png")
        pd.DataFrame({"customer_id": target.customer_id.values, "ap_at_12": aps}).to_csv(OUT / "confirmation_user_ap.csv", index=False)
        metadata.update(selected=folder.name, confirmation_map=float(aps.mean()), zero_ap_users=int((aps == 0).sum()))
    pd.DataFrame([{key: trial.get(key) for key in ["candidate", "island", "status", "score", "error"]} for trial in trials]).to_csv(OUT / "trials.csv", index=False)
    (OUT / "metadata.json").write_text(json.dumps(metadata, indent=2))
    stage_note = ("Полная каталожная оценка приостановлена пользователем. Оценка на общих кандидатах — [отдельный отчёт](../shared_idgnn/report.md)."
                  if catalog_paused else "Полная оценка val/test ещё выполняется.")
    text = ["# Ход поиска признаков LLM-FE v2", "", "Промежуточные validation-результаты. " + stage_note, "",
            "![MAP по попыткам и confirmation](search_progress.png)", "",
            "![Успешные и отклонённые попытки](attempts_histogram.png)", "",
            "![Важность признаков](feature_importance.png)", "",
            "![Распределение AP пользователей](ap_histogram.png)", "",
            "Кривые loss по итерациям LightGBM текущий запуск не сохранял.", "",
            "Обновить: `RelBenchGNN/.venv-wsl/bin/python LLMFeatures/plot_progress.py`.", ""]
    (OUT / "index.md").write_text("\n".join(text), encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
