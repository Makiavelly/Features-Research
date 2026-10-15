"""Resumable LLM-FE adaptation: 3 islands, validation MAP, no test feedback."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

import numpy as np
import requests

from features import FeatureEngine, ROOT, ITEM_COLUMNS, USER_COLUMNS, validate_program, digest
from evaluate import OUT, CACHE, RUN, train_pairs, atomic_json
sys.path.insert(0, str(ROOT / "RelBenchGNN"))
from tracking import record
from relbench import load_dataset

MODEL = "qwen2.5-coder:7b-instruct-q4_K_M"
URL = "http://127.0.0.1:11435"
CONFIG = {"schema_version": 1, "run_id": RUN, "seed": 42, "llm": MODEL,
          "backend": "Ollama 0.21.0 (llama.cpp runner)", "quantization": "Q4_K_M",
          "context_tokens": 4096, "generation_tokens": 1800, "temperature": .8,
          "islands": 3, "llm_samples": 20, "memory_programs_per_prompt": 1,
          "train_user_times": 50000, "negative_sampling": "same saved pairs as manual_v1; only IDs/time/labels reused",
          "pair_selection_seed": 2026,
          "search_validation_users": 256, "confirmation_validation_users": 1024,
          "confirmation_candidates": 3, "search_objective": "full-catalog MAP@12",
          "final": "all validation and test users; full catalog and saved ID-GNN pools",
          "downstream": "LightGBM binary, 31 leaves, 150 rounds, same fixed settings for every program",
          "inputs": "raw static fields plus LLM SQL aggregates/derived features; no manual/GNN features",
          "feature_program": "restricted SQL expression AST-equivalent interface, not arbitrary Python",
          "cutoff": "t_dat <= prediction timestamp", "search_timeout_seconds": 21600,
          "final_timeout_seconds": 604800, "training_embeddings": False,
          "paper_deviations": ["temporal relational ranking, MAP@12, LightGBM",
                               "SQL expression programs and controlled host joins instead of Python",
                               "one prior program per prompt, 3 islands, 20 LLM proposals",
                               "256 search users, disjoint 1024 confirmation users; complete catalog",
                               "50k user-times, fixed seed42, no ensemble"]}

INSTRUCTION = """You design features for H&M recommendation: rank 105542 clothing articles for each customer at cutoff; predict purchases in the NEXT 7 days. Fitness is downstream LightGBM validation MAP@12 over the COMPLETE catalog, not classification accuracy. Generate ONE COMPLETE feature program as JSON. Use domain knowledge to discover useful nontrivial features, improve and combine previous successful programs. No pretrained embedding or human-engineered historical feature is provided.

JSON format:
{"rationale":"brief hypothesis","aggregates":[{"name":"f_unique_name","keys":["customer_id"],"sql":"DuckDB aggregate expression"}],"derived":[{"name":"f_another_name","sql":"scalar expression over raw and aggregate feature names"}]}

The host supplies a time-safe history relation; rows with transactions AFTER cutoff are physically excluded. Columns: price (normalized transaction price), sales_channel_id (1/2), days_ago (integer days since transaction), customer_age, product_code, product_type_no, graphical_appearance_no, colour_group_code, perceived_colour_value_id, perceived_colour_master_id, department_no, index_group_no, section_no, garment_group_no. These last columns describe the purchased article. Missing values can occur.
Aggregate keys can be [customer_id], [article_id], [customer_id,article_id], or [customer_id,ONE article category column]. The host computes GROUP BY and joins results to each candidate using matching keys. IDs are grouping keys ONLY, never numerical features. Each SQL is an expression, not a query. FILTER (WHERE ...) is supported. Choose time windows yourself using days_ago. Functions allowed: count,sum,avg,min,max,stddev_pop,median,quantile_cont,approx_count_distinct,mode,coalesce,nullif,abs,sqrt,ln,log,power,greatest,least,round,floor,ceil,cast. count(*) is allowed. Never count IDs directly; use count(*) or category diversity.
Derived scalar expressions may use aggregate feature names plus raw_u_age, raw_u_fn, raw_u_active, raw_u_club_member_status, raw_u_fashion_news_frequency and raw_i_ followed by one article column listed above. Derived features can refer to earlier derived entries. SQL CASE WHEN is allowed. Use NULLIF for division. No quoted strings, SELECT, FROM, subqueries, window functions, table access, target labels or timestamps. Do not invent columns. Do not use features from later data. The host fills remaining missing/inf with -1. Every program starts from original raw fields and must specify its complete chosen feature set, not additions to prior code. Keep JSON concise: normally 8-16 aggregates and 2-6 derived features, at most 24/12. Return only JSON, no markdown.
"""


def evaluate(directory, stage):
    file = directory / f"{stage}_metrics.json"
    if file.exists():
        return json.loads(file.read_text())
    with (directory / f"{stage}.log").open("a") as log:
        try:
            process = subprocess.Popen([sys.executable, "-u", str(ROOT / "LLMFeatures/evaluate.py"),
                                        "--directory", str(directory), "--stage", stage],
                                       stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            (directory / f"{stage}.pid").write_text(str(process.pid))
            code = process.wait(timeout=CONFIG["final_timeout_seconds"] if stage == "final" else CONFIG["search_timeout_seconds"])
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, __import__('signal').SIGTERM)
            process.wait(timeout=30)
            raise RuntimeError("Evaluator exceeded wall-clock limit")
    if code != 0:
        tail = (directory / f"{stage}.log").read_text()[-5000:]
        raise RuntimeError(f"Evaluator exited {code}: {tail}")
    return json.loads(file.read_text())


def examples():
    engine = FeatureEngine(CACHE / "examples")
    pairs = train_pairs().sample(n=5, random_state=42)
    engine.prepare(pairs.timestamp.iloc[0], pairs.customer_id.values, {"aggregates": [], "derived": []})
    frame = engine.frame(pairs)
    frame["training_label"] = pairs.label.to_numpy()
    engine.close()
    return frame.to_json(orient="records")


def generate(directory, sample_index, memory, data_examples, last_error):
    response_file = directory / "llm_response.json"
    if response_file.exists():
        response = json.loads(response_file.read_text())
    else:
        prompt = INSTRUCTION + "\nFive TRAIN examples (raw fields and label):\n" + data_examples
        if memory:
            best = max(memory, key=lambda item: item["score"])
            prior = json.loads((Path(best["directory"]) / "program.json").read_text())
            prompt += "\nPrevious successful complete program and validation MAP (fraction):\n"
            prompt += json.dumps({"score": best["score"], "program": prior}, separators=(",", ":"))
        if last_error:
            prompt += "\nPrevious rejected proposal error (avoid repeating): " + last_error[-800:]
        (directory / "prompt.txt").write_text(prompt)
        record("llmfe_generating", f"Локальная LLM предлагает программу {sample_index+1}/20", RUN,
               status="generating", candidate=sample_index+1)
        response = requests.post(URL + "/api/generate", timeout=(30, 3600), json={
            "model": MODEL, "prompt": prompt, "format": "json", "stream": False, "keep_alive": "30m",
            "options": {"seed": 42+sample_index, "temperature": .8, "num_ctx": 4096,
                        "num_predict": 1800, "num_thread": 4}})
        response.raise_for_status()
        response = response.json()
        atomic_json(response_file, response)
        if response.get("done_reason") == "length":
            raise ValueError("LLM program truncated at generation token limit")
        if response.get("prompt_eval_count", 0) + response.get("eval_count", 0) > 4096:
            raise ValueError("Prompt exceeded configured context")
    program = validate_program(json.loads(response["response"]))
    if not program.get("aggregates") and not program.get("derived"):
        raise ValueError("LLM returned no new features")
    atomic_json(directory / "program.json", program)
    return program


def report(final_directory, results, trials):
    destination = ROOT / "reports/llmfe_qwen25coder7b_v1"
    destination.mkdir(parents=True, exist_ok=True)
    metrics = json.loads((final_directory / "final_metrics.json").read_text())
    reference = json.loads((ROOT / "RelBenchGNN/results/seed_42/metrics.json").read_text())
    checks = json.loads((final_directory / "verification.json").read_text())
    if not checks["passed"]:
        raise RuntimeError("Independent inference verification failed")
    rows = ["# LLM-FE: local Qwen2.5-Coder-7B → LightGBM", "",
            "MAP@12 в процентах; seed 42. Адаптация LLM-FE к временному H&M ranking.", "",
            "| Метод / протокол | Validation | Test |", "|---|---:|---:|"]
    rows.append(f"| ID-GNN, исходный конвейер | {100*reference['val_metrics']['map']:.5f} | {100*reference['test_metrics']['map']:.5f} |")
    for prefix, label in [("", "LLM-FE, полный каталог"), ("shared_", "LLM-FE, кандидаты ID-GNN")]:
        rows.append(f"| {label} | {100*metrics[prefix+'val_metrics']['map']:.5f} | {100*metrics[prefix+'test_metrics']['map']:.5f} |")
    rows += ["", "Исходный ID-GNN заполняет нулями оценки вне sampled-подграфа. Общие кандидаты — отдельная проверка ранжирования.",
             "Сохранены те же 50,000 train user-time строк / отрицательные пары, что manual_v1; ручные/GNN признаки не использовались.",
             "Входы: сырые статические поля плюс SQL-признаки, предложенные локальной LLM. Budget обучения ID-GNN больше.",
             "Поиск: 20 предложений, 3 острова, MAP на 256 validation пользователях по всему каталогу;",
             "до 3 лучших программ проверены на других 1024 validation пользователях. Test не участвовал в выборе.",
             "Проверка повторного инференса в отдельном процессе выполнена на подмножестве пользователей; её охват указан в verification.json.",
             "Это один seed и ограниченный язык SQL-программ; результат не обобщается на все LLM или все способы генерации признаков.",
             "", f"Выбранная программа: `{final_directory.relative_to(ROOT)}/program.json`.", "",
             "Источники: https://arxiv.org/html/2503.14434v3 ; https://github.com/nikhilsab/LLMFE", ""]
    (destination / "report.md").write_text("\n".join(rows), encoding="utf-8")
    atomic_json(destination / "report.json", {"final": True, "metrics": metrics, "verification": checks,
                                             "trials": trials, "confirmation": results, "config": CONFIG})
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    labels = ["ID-GNN", "LLM-FE full catalog", "LLM-FE ID-GNN pool"]
    values = [100*reference["test_metrics"]["map"], 100*metrics["test_metrics"]["map"], 100*metrics["shared_test_metrics"]["map"]]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(labels, values)
    ax.set_xlabel("Test MAP@12 (%)")
    fig.tight_layout()
    fig.savefig(destination / "comparison.png", dpi=160)
    plt.close(fig)
    record("llmfe_complete", "LLM-FE завершён: полный каталог, общие кандидаты и отдельная проверка инференса", RUN,
           status="complete", val_metrics=metrics["val_metrics"], test_metrics=metrics["test_metrics"],
           shared_val_metrics=metrics["shared_val_metrics"], shared_test_metrics=metrics["shared_test_metrics"],
           artifacts=str(destination.relative_to(ROOT)))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    lock = (OUT / "run.lock").open("a")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    (OUT / "pipeline.pid").write_text(str(os.getpid()))
    config_path = OUT / "config.json"
    if config_path.exists() and json.loads(config_path.read_text()) != CONFIG:
        raise RuntimeError("Config changed: new run_id/output directory required")
    atomic_json(config_path, CONFIG)
    source_manifest = OUT / "source_manifest.json"
    if not source_manifest.exists():
        sources = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in (ROOT / "LLMFeatures").glob("*.py")}
        pairs_file = CACHE / "train_pairs.parquet"
        pairs = train_pairs()
        if len(pairs) != 803377 or len(pairs[["customer_id", "timestamp"]].drop_duplicates()) != 50000:
            raise RuntimeError("Training pair budget differs from the documented control")
        atomic_json(source_manifest, {"source_sha256": sources,
            "data_manifest_sha256": hashlib.sha256((ROOT / "data/download_manifest.json").read_bytes()).hexdigest(),
            "train_pairs_sha256": hashlib.sha256(pairs_file.read_bytes()).hexdigest(),
            "model_manifest_sha256": hashlib.sha256((OUT / "model_manifest.json").read_bytes()).hexdigest()})
        del pairs
    record("llmfe_start", "Начат поиск LLM-признаков Qwen2.5-Coder-7B с полным каталогом", RUN,
           status="preparing", config=CONFIG, artifacts=str(OUT.relative_to(ROOT)))
    task = load_dataset(ROOT / "data/rel-hm").load_task("user-item-purchase")
    val = task.get_table("val")
    selection = OUT / "validation_selection.npz"
    if not selection.exists():
        order = np.random.default_rng(42).permutation(len(val.df))
        np.savez(selection, search=np.sort(order[:256]), confirm=np.sort(order[256:1280]))
    data_examples = examples()
    empty = {"rationale": "Raw static feature control; no LLM features", "aggregates": [], "derived": []}
    control = OUT / "raw_control"
    control.mkdir(exist_ok=True)
    atomic_json(control / "program.json", empty)
    baseline = evaluate(control, "search")
    record("llmfe_control", "Контроль сырых признаков оценён на search validation по всему каталогу", RUN,
           status="searching", raw_search_val_metrics=baseline["val_metrics"])
    islands = [[{"directory": str(control), "score": baseline["val_metrics"]["map"]}] for _ in range(3)]
    trials = []
    errors = ["", "", ""]
    for index in range(20):
        island = index % 3
        directory = OUT / "candidates" / f"candidate_{index+1:02d}"
        directory.mkdir(parents=True, exist_ok=True)
        trial_path = directory / "trial.json"
        if trial_path.exists():
            trial = json.loads(trial_path.read_text())
        else:
            try:
                program = generate(directory, index, islands[island], data_examples, errors[island])
                if index == 0:
                    smoke = evaluate(directory, "smoke")
                    record("llmfe_smoke", "LLM-программа прошла SQL/train/full-catalog smoke; это не итоговые метрики", RUN,
                           status="searching", smoke=smoke)
                metrics = evaluate(directory, "search")
                trial = {"candidate": index+1, "island": island, "status": "valid",
                         "score": metrics["val_metrics"]["map"], "directory": str(directory),
                         "program_sha256": digest(program), "metrics": metrics}
            except Exception as error:
                trial = {"candidate": index+1, "island": island, "status": "rejected", "error": str(error),
                         "directory": str(directory)}
                (directory / "error.txt").write_text(traceback.format_exc())
            atomic_json(trial_path, trial)
        trials.append(trial)
        if trial["status"] == "valid":
            islands[island].append(trial)
            errors[island] = ""
        else:
            errors[island] = trial["error"]
        atomic_json(OUT / "search_state.json", {"completed_proposals": len(trials), "islands": islands, "trials": trials})
        progress_lines = ["# LLM-FE: промежуточный поиск", "",
                          "Это search validation, не полные validation/test метрики.", "",
                          "| Предложение | Остров | Статус | Search MAP@12, % |",
                          "|---|---|---|---:|"]
        for item in trials:
            value = f"{100*item['score']:.5f}" if item["status"] == "valid" else "—"
            progress_lines.append(f"| {item['candidate']} | {item['island']} | {item['status']} | {value} |")
        (OUT / "progress.md").write_text("\n".join(progress_lines)+"\n", encoding="utf-8")
        record("llmfe_trial", f"LLM-FE программа {index+1}/20: {trial['status']}", RUN,
               status="searching", completed_proposals=len(trials), trial=trial)
    # Unload only our server's model before the final CPU evaluation.
    requests.post(URL + "/api/generate", json={"model": MODEL, "keep_alive": 0}, timeout=60)
    valid = sorted([trial for trial in trials if trial["status"] == "valid"], key=lambda item: item["score"], reverse=True)
    if not valid:
        raise RuntimeError("All 20 LLM proposals were rejected; inspect saved outputs/errors")
    unique = []
    seen = set()
    for trial in valid:
        if trial["program_sha256"] not in seen:
            unique.append(trial)
            seen.add(trial["program_sha256"])
    confirmations = []
    for trial in unique[:3]:
        directory = Path(trial["directory"])
        metrics = evaluate(directory, "confirm")
        confirmations.append({"directory": str(directory), "score": metrics["val_metrics"]["map"], "metrics": metrics})
        atomic_json(OUT / "confirmation.json", confirmations)
    best = max(confirmations, key=lambda item: item["score"])
    best_path = Path(best["directory"])
    atomic_json(OUT / "selected.json", {"directory": str(best_path), "confirmation_score": best["score"],
                                        "selection": "validation only; no test feedback"})
    record("llmfe_selected", "Программа выбрана по отдельной confirmation validation; начата полная оценка", RUN,
           status="evaluating", selection=best)
    final = evaluate(best_path, "final")
    with (best_path / "verification.log").open("a") as log:
        subprocess.run([sys.executable, "-u", str(ROOT / "LLMFeatures/verify.py"), str(best_path)],
                       stdout=log, stderr=subprocess.STDOUT, check=True)
    report(best_path, confirmations, trials)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        record("llmfe_failure", "LLM-FE остановлен с ошибкой; артефакты и прогресс сохранены", RUN,
               status="failed", error=str(error))
        raise
