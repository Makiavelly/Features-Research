"""Resumable H002: successful distinct sets and LLM requests have separate budgets."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time
import traceback
from h002_common import ROOT, RUN, OUT, CACHE, OLD, CONFIG
from evaluate import atomic_json, train_pairs
from features import FeatureEngine, validate_program
from run import INSTRUCTION, examples, URL
from tracking import record
import numpy as np
import requests

GUIDANCE = """
INTERFACE CLARIFICATION: Aggregate SQL sees history columns including days_ago, price,
sales_channel_id, customer_age and article categories. Derived SQL NEVER sees these
history columns: it sees only raw_u_*, raw_i_*, aggregate names and earlier derived names.
No OVER/window functions. The host performs grouping; SQL expressions do not include GROUP BY.
Use only grouping key patterns listed above. Emit numeric values, no quoted strings.
Do not emit feature_importance, metadata or extra keys. Keep about 6-10 aggregates and
2-4 derived entries so the complete program fits 1800 tokens. Formulas must be yours.
For this run fitness is MAP@12 on FIXED ID-GNN CANDIDATES for 256 validation customers,
NOT full catalog. All proposals use the same customers and pools. Training uses 803377
sampled pairs. Return a complete program, not a patch.
"""


def program_key(program):
    """Ignore explanation, feature names, group order and harmless SQL whitespace/case."""
    definitions = {}
    signatures = []
    for entry in program.get("aggregates", []) + program.get("derived", []):
        sql = entry["sql"].lower()
        for name in sorted(definitions, key=len, reverse=True):
            sql = re.sub(r"\b" + re.escape(name) + r"\b", "(" + definitions[name] + ")", sql)
        sql = re.sub(r"\s+", "", sql)
        signature = json.dumps([sorted(entry.get("keys", [])), sql], separators=(",", ":"))
        definitions[entry["name"]] = signature
        signatures.append(signature)
    return hashlib.sha256(json.dumps(sorted(set(signatures))).encode()).hexdigest()


def evaluate(directory, stage):
    path = directory / ("verification.json" if stage == "replay" else stage + "_metrics.json")
    if path.exists():
        return json.loads(path.read_text())
    with (directory / (stage + ".log")).open("a") as log:
        child = subprocess.Popen([sys.executable, "-u", str(ROOT / "LLMFeatures/h002_evaluate.py"),
                                  "--directory", str(directory), "--stage", stage],
                                 stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        (directory / (stage + ".pid")).write_text(str(child.pid))
        try:
            code = child.wait(timeout=21600)
        except BaseException:
            if child.poll() is None:
                os.killpg(child.pid, signal.SIGTERM)
                child.wait(timeout=30)
            raise
    if code:
        raise RuntimeError((directory / (stage + ".log")).read_text()[-2000:])
    return json.loads(path.read_text())


def progress(trials):
    successful = [t for t in trials if t["status"] == "valid"]
    state = {"calls": len(trials), "repairs": sum(t["repair"] > 0 for t in trials),
             "evaluated_distinct": len(successful), "trials": trials,
             "target": 20, "max_calls": 100}
    atomic_json(OUT / "search_state.json", state)
    lines = ["# H002: ход поиска", "", "Общие кандидаты ID-GNN; это search, не итоговые метрики.",
             f"Обращения: {len(trials)}/100. Различные оценённые наборы: {len(successful)}/20.", "",
             "| Запрос | Исправление | Статус | Search MAP, % |", "|---|---:|---|---:|"]
    for t in trials:
        value = f"{100*t['score']:.5f}" if t["status"] == "valid" else "—"
        lines.append(f"| {t['call']} | {t['repair']} | {t['status']} | {value} |")
    (OUT / "progress.md").write_text("\n".join(lines), encoding="utf-8")
    from h002_plot import search_plots
    search_plots(state)
    return successful


def prepare():
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    if (OUT / "config.json").exists() and json.loads((OUT / "config.json").read_text()) != CONFIG:
        raise RuntimeError("Configuration changed: use a new run ID")
    atomic_json(OUT / "config.json", CONFIG)
    if not (OUT / "validation_selection.npz").exists():
        shutil.copy2(OLD / "validation_selection.npz", OUT / "validation_selection.npz")
    selection = np.load(OUT / "validation_selection.npz")
    assert len(selection['search']) == 256 and len(selection['confirm']) == 1024
    assert not np.intersect1d(selection['search'], selection['confirm']).size
    if not (CACHE / "train_pairs.parquet").exists():
        shutil.copy2(ROOT / "baseline/cache/llmfe_qwen25coder7b_v2/train_pairs.parquet", CACHE / "train_pairs.parquet")
    pairs = train_pairs()
    assert len(pairs) == 803377 and len(pairs[["customer_id", "timestamp"]].drop_duplicates()) == 50000
    tags = requests.get(URL + "/api/tags", timeout=10).json()
    model = next(m for m in tags['models'] if m['name'] == CONFIG['llm'])
    assert model['digest'] == CONFIG['model_digest']
    atomic_json(OUT / "model_manifest.json", model)
    if not (OUT / "source_manifest.json").exists():
        files = list((ROOT / "LLMFeatures").glob("*.py")) + [CACHE / "train_pairs.parquet", OUT / "validation_selection.npz", ROOT / "data/download_manifest.json"]
        files += list((ROOT / "RelBenchGNN/results/seed_42/inference").glob("*_candidates.parquet"))
        atomic_json(OUT / "source_manifest.json", {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files})


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lock = (OUT / "run.lock").open("a")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    (OUT / "pipeline.pid").write_text(str(os.getpid()))
    prepare()
    if (OUT / "complete.json").exists():
        return
    record("h002_start", "H002: 20 различных оценённых наборов, до100 запросов, до2 исправлений; поиск на общих кандидатах, LightGBM8 потоков", RUN,
           status="preparing", config=CONFIG, artifacts=str(OUT.relative_to(ROOT)))
    raw = OUT / "raw_control"
    raw.mkdir(exist_ok=True)
    atomic_json(raw / "program.json", {"rationale": "raw control", "aggregates": [], "derived": []})
    baseline = evaluate(raw, "search")
    memory = [[{"directory": str(raw), "score": baseline['val_metrics']['map']} ] for _ in range(3)]
    data_examples = examples()
    trials = []
    repair = 0
    proposal = 0
    previous = None
    while len([t for t in trials if t['status'] == 'valid']) < 20 and len(trials) < 100:
        number = len(trials) + 1
        island = proposal % 3
        directory = OUT / "candidates" / f"candidate_{number:03d}"
        directory.mkdir(parents=True, exist_ok=True)
        trial_path = directory / "trial.json"
        if trial_path.exists():
            trial = json.loads(trial_path.read_text())
        else:
            trial = {"call": number, "proposal": proposal, "island": island, "repair": repair,
                     "directory": str(directory), "parent_call": previous['call'] if repair else None}
            tick = time.perf_counter()
            response = None
            try:
                # The old instruction's full-catalog fitness is replaced explicitly.
                instruction = INSTRUCTION.replace("over the COMPLETE catalog", "over FIXED ID-GNN candidate pools")
                prompt = instruction + GUIDANCE + "\nTRAIN examples:\n" + data_examples
                if repair:
                    parent = Path(previous['directory'])
                    bad = json.loads((parent / "llm_response.json").read_text()).get('response', '') if (parent / "llm_response.json").exists() else ''
                    prompt += "\nREPAIR this entire proposal:\n" + bad + "\nExact rejection:\n" + previous['error'][-1500:]
                else:
                    best = max(memory[island], key=lambda x: x['score'])
                    prior = json.loads((Path(best['directory']) / "program.json").read_text())
                    prompt += "\nPrevious best complete program and search MAP fraction:\n" + json.dumps({"score": best['score'], "program": prior}, separators=(',', ':'))
                (directory / "prompt.txt").write_text(prompt)
                atomic_json(directory / "request.json", {**trial, "seed": 42 + number - 1})
                record("h002_generating", f"H002 запрос{number}/100, оценено{len([t for t in trials if t['status']=='valid'])}/20, исправление{repair}", RUN,
                       status="generating", llm_calls=number, evaluated_distinct=sum(t['status']=='valid' for t in trials))
                response_path = directory / "llm_response.json"
                if response_path.exists():
                    response = json.loads(response_path.read_text())
                else:
                    result = requests.post(URL + "/api/generate", timeout=(30, 3600), json={
                        "model": CONFIG['llm'], "prompt": prompt, "format": "json", "stream": False, "keep_alive": "30m",
                        "options": {"seed": 42+number-1, "temperature": .8, "num_ctx": 4096, "num_predict": 1800, "num_thread": 4}})
                    result.raise_for_status()
                    response = result.json()
                    atomic_json(response_path, response)
                trial['prompt_tokens'] = response.get('prompt_eval_count', 0)
                trial['generated_tokens'] = response.get('eval_count', 0)
                trial['llm_seconds'] = response.get('total_duration', 0) / 1e9
                if response.get('done_reason') == 'length':
                    raise ValueError("Generation truncated at 1800 tokens; return a smaller complete program")
                if trial['prompt_tokens'] + trial['generated_tokens'] > 4096:
                    raise ValueError("Context capacity exceeded")
                program = validate_program(json.loads(response['response']))
                if not program.get('aggregates') and not program.get('derived'):
                    raise ValueError("No new features")
                atomic_json(directory / "program.json", program)
                trial['program_sha256'] = program_key(program)
                if trial['program_sha256'] in {t.get('program_sha256') for t in trials if t['status']=='valid'}:
                    trial.update(status="duplicate", error="Duplicate of an already evaluated feature set; propose distinct formulas")
                else:
                    # Catch real binder/type errors cheaply before full training.
                    engine = FeatureEngine(CACHE / "preflight")
                    try:
                        sample = train_pairs().sort_values('timestamp').tail(512)
                        engine.prepare(sample.timestamp.iloc[0], sample.customer_id.values, program)
                        engine.matrix(sample)
                    finally:
                        engine.close()
                    metrics = evaluate(directory, "search")
                    trial.update(status="valid", score=metrics['val_metrics']['map'], metrics=metrics)
            except Exception as error:
                trial.update(status="rejected", error=str(error))
                (directory / "error.txt").write_text(traceback.format_exc())
            trial['elapsed_seconds'] = time.perf_counter() - tick
            atomic_json(trial_path, trial)
        trials.append(trial)
        successful = progress(trials)
        record("h002_trial", f"H002 запрос{number}: {trial['status']}; различных оценённых{len(successful)}/20", RUN,
               status="searching", llm_calls=len(trials), evaluated_distinct=len(successful), trial=trial)
        if trial['status'] == 'valid':
            memory[island].append(trial)
        if trial['status'] != 'valid' and repair < 2:
            repair += 1
            previous = trial
        else:
            proposal += 1
            repair = 0
            previous = None
    valid = sorted([t for t in trials if t['status']=='valid'], key=lambda x: x['score'], reverse=True)
    if not valid:
        raise RuntimeError("No evaluated programs; budget exhausted")
    requests.post(URL + "/api/generate", json={"model": CONFIG['llm'], "keep_alive": 0}, timeout=60).raise_for_status()
    confirmations = []
    for trial in valid[:3]:
        metrics = evaluate(Path(trial['directory']), "confirm")
        confirmations.append({"directory": trial['directory'], "score": metrics['val_metrics']['map'], "metrics": metrics})
        atomic_json(OUT / "confirmation.json", confirmations)
    selected = max(confirmations, key=lambda x: x['score'])
    atomic_json(OUT / "selected.json", {**selected, "selection": "disjoint validation confirmation only; frozen before test"})
    record("h002_selected", "H002: признаки выбраны по confirmation; начата итоговая оценка на общих кандидатах", RUN, status="evaluating", selection=selected)
    directory = Path(selected['directory'])
    final = evaluate(directory, "final")
    check = evaluate(directory, "replay")
    from h002_plot import final_report
    final_report(final, check, trials, selected)
    atomic_json(OUT / "complete.json", {"metrics": final, "verification": check, "target_met": len(valid)==20})
    record("h002_complete", "H002 завершён: итоговые shared MAP, независимый полный повтор и графики сохранены", RUN,
           status="complete", val_metrics=final['val_metrics'], test_metrics=final['test_metrics'],
           llm_calls=len(trials), evaluated_distinct=len(valid), target_met=len(valid)==20,
           artifacts="reports/llmfe_h002_shared_v1")


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    try:
        main()
    except Exception as error:
        record("h002_failed", "H002 остановлен с ошибкой; прогресс сохранён", RUN, status="failed", error=str(error))
        raise
