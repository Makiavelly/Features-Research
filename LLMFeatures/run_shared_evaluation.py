"""Evaluate frozen selected model on the exact saved ID-GNN candidate pools."""
import fcntl
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import lightgbm as lgb
import numpy as np
import pandas as pd
from relbench import load_dataset

import evaluate as evaluation
from evaluate import OUT, CACHE, atomic_json, shared_candidates, load_execution_settings
from features import ROOT, FeatureEngine
sys.path.insert(0, str(ROOT / "RelBenchGNN"))
from tracking import record

RUN = "hm_llmfe_qwen25coder7b_seed42_v2_shared_idgnn_inference_v1"
DEST = OUT / "shared_idgnn"
REPORT = ROOT / "reports/llmfe_qwen25coder7b_v2/shared_idgnn"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def score(verify=False):
    model_directory = Path(json.loads((OUT / "selected.json").read_text())["directory"])
    model = lgb.Booster(model_file=str(model_directory / "model.txt"))
    program = json.loads((model_directory / "program.json").read_text())
    load_execution_settings(model_directory)
    if verify:
        evaluation.PREDICT_THREADS = 2
    destination = DEST / "replay" if verify else DEST
    destination.mkdir(parents=True, exist_ok=True)
    engine = FeatureEngine(CACHE / ("shared_replay" if verify else "shared_score"))
    task = load_dataset(ROOT / "data/rel-hm").load_task("user-item-purchase")
    result = {"run_id": RUN, "seed": 42, "protocol": "exact saved ID-GNN seed42 candidate pools",
              "model_directory": str(model_directory.relative_to(ROOT)),
              "model_sha256": sha(model_directory / "model.txt"),
              "program_sha256": sha(model_directory / "program.json"),
              "selection": "previously selected candidate08 using validation only; no new selection",
              "inference_from_saved_model": True, "prediction_threads": evaluation.PREDICT_THREADS,
              "full_catalog_evaluation": "paused by user; incomplete predictions excluded"}
    reference = json.loads((DEST / "metrics.json").read_text()) if verify else None
    for split in ["val", "test"]:
        table = task.get_table(split)
        candidate_file = ROOT / f"RelBenchGNN/results/seed_42/inference/{split}_candidates.parquet"
        candidates = pd.read_parquet(candidate_file)
        if not np.array_equal(candidates.customer_id.values, table.df.customer_id.values):
            raise RuntimeError("Candidate/user alignment mismatch")
        started = time.perf_counter()
        predictions = shared_candidates(engine, program, model, table, destination, split)
        if not all(len(np.unique(pred)) == 12 and np.isin(pred, pool).all()
                   for pred, pool in zip(predictions, candidates.candidates)):
            raise RuntimeError("Predictions outside shared pool or duplicate IDs")
        seconds = time.perf_counter()-started
        metrics = task.evaluate(predictions) if split == "test" else task.evaluate(predictions, table)
        native = np.load(ROOT / f"RelBenchGNN/results/seed_42/{split}_predictions.npy")
        if not all(np.isin(pred, pool).all() for pred, pool in zip(native, candidates.candidates)):
            raise RuntimeError("ID-GNN predictions outside saved candidate pool")
        native_metrics = task.evaluate(native) if split == "test" else task.evaluate(native, table)
        result[split] = {"users": len(table.df), "pairs": int(candidates.candidates.map(len).sum()),
                         "candidate_file_sha256": sha(candidate_file), "metrics": metrics,
                         "idgnn_metrics_recomputed": native_metrics, "seconds": seconds}
        if verify:
            expected = np.load(DEST / f"shared_{split}_predictions.npy")
            if not np.array_equal(predictions, expected) or metrics != reference[split]["metrics"]:
                raise RuntimeError(f"Independent replay mismatch on {split}")
            result[split]["predictions_identical"] = True
        print(json.dumps({"split": split, **result[split]}), flush=True)
        record("llmfe_shared_split", f"LLM-FE общие кандидаты: {split} {'перепроверен' if verify else 'оценён'}", RUN,
               status="verifying" if verify else "evaluating", split=split, split_result=result[split])
    engine.close()
    if verify:
        result["passed"] = True
        result["coverage"] = "all validation/test users and exact shared candidate pools, independent process, 2 CPU threads"
    atomic_json(DEST / ("verification.json" if verify else "metrics.json"), result)
    return result


def report():
    metrics = json.loads((DEST / "metrics.json").read_text())
    check = json.loads((DEST / "verification.json").read_text())
    if not check["passed"]:
        raise RuntimeError("Replay not verified")
    REPORT.mkdir(parents=True, exist_ok=True)
    manual = json.loads((ROOT / "baseline/results/manual_v1/lightgbm/seed_42/metrics.json").read_text())
    tree = json.loads((ROOT / "baseline/results/manual_v1/decision_tree/seed_42/metrics.json").read_text())
    rows = [
        ("ID-GNN", metrics["val"]["idgnn_metrics_recomputed"]["map"], metrics["test"]["idgnn_metrics_recomputed"]["map"]),
        ("LightGBM: ручные признаки", manual["val_metrics"]["map"], manual["test_metrics"]["map"]),
        ("LightGBM: признаки LLM + сырые поля", metrics["val"]["metrics"]["map"], metrics["test"]["metrics"]["map"]),
        ("DecisionTree: ручные признаки", tree["val_metrics"]["map"], tree["test_metrics"]["map"])]
    frame = pd.DataFrame(rows, columns=["model", "val_map", "test_map"])
    frame.to_csv(REPORT / "comparison.csv", index=False)
    lines = ["# LLM-FE: оценка на общих кандидатах ID-GNN", "",
             "Проверенная полная оценка этого протокола: все validation/test пользователи, seed42.",
             "Полная каталожная оценка приостановлена пользователем; её неполные результаты сюда не включены.", "",
             "| Модель | Validation MAP@12, % | Test MAP@12, % |", "|---|---:|---:|"]
    lines += [f"| {name} | {100*val:.5f} | {100*test:.5f} |" for name,val,test in rows]
    lines += ["", "![Сравнение](comparison.png)", "",
              f"Validation: {metrics['val']['users']:,} пользователей / {metrics['val']['pairs']:,} пар.",
              f"Test: {metrics['test']['users']:,} пользователей / {metrics['test']['pairs']:,} пар.",
              "Кандидаты и порядок пользователей точно совпадают с сохранённым инференсом ID-GNN seed42.",
              "Полный независимый повтор из сохранённой модели на 2 CPU-потоках воспроизвёл все top-12 и MAP.",
              "Обучение/поиск не повторялись. Выбран прежний candidate08 до чтения test-результатов.",
              "LLM-LightGBM и ручной LightGBM используют те же 803,377 train пар / 50,000 user-times; ID-GNN обучалась с большим бюджетом.",
              "Протоколы подбора и производные seeds LightGBM различаются: это сопоставление конвейеров, не строго изолированный эффект признаков.",
              "LLM-признаки включают сырые статические поля; ручные агрегаты и GNN-представления не используются.",
              "При равных scores LightGBM использует article_id ascending. Показан один seed, без оценки устойчивости.", ""]
    (REPORT / "report.md").write_text("\n".join(lines), encoding="utf-8")
    atomic_json(REPORT / "report.json", {"final_for_shared_protocol": True, "full_catalog_final": False,
                                         "metrics": metrics, "verification": check, "comparison": frame.to_dict("records")})
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 5))
    index = np.arange(len(rows))
    ax.barh(index-.18, 100*frame.val_map, height=.36, label="Validation")
    ax.barh(index+.18, 100*frame.test_map, height=.36, label="Test")
    ax.set_yticks(index, frame.model)
    ax.invert_yaxis()
    ax.set_xlabel("MAP@12, %")
    ax.set_title("Одинаковые кандидаты ID-GNN, seed42")
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORT / "comparison.png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    record("llmfe_shared_complete", "LLM-LightGBM оценён на общих кандидатах ID-GNN; полный повтор подтвердил предсказания", RUN,
           status="complete", val_metrics=metrics["val"]["metrics"], test_metrics=metrics["test"]["metrics"],
           artifacts=str(REPORT.relative_to(ROOT)))
    print(frame.to_string(index=False), flush=True)


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    if "--verify" in sys.argv:
        score(verify=True)
        return
    lock = (DEST / "pipeline.lock").open("a")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    (DEST / "pipeline.pid").write_text(str(__import__('os').getpid()))
    record("llmfe_shared_start", "Начата отдельная оценка выбранного LLM-LightGBM на общих кандидатах ID-GNN", RUN,
           status="evaluating", artifacts=str(DEST.relative_to(ROOT)))
    score()
    with (DEST / "verification.log").open("a") as log:
        subprocess.run([sys.executable, "-u", str(Path(__file__).resolve()), "--verify"],
                       stdout=log, stderr=subprocess.STDOUT, check=True)
    report()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        record("llmfe_shared_failure", "Оценка общих кандидатов остановилась с ошибкой", RUN, status="failed", error=str(error))
        raise
