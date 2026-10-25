"""After selected runs: reload best checkpoints, verify inference and render report."""
import json
from pathlib import Path
import subprocess
import sys

from tracking import record
from experiment_plan import selected_seeds

ROOT = Path(__file__).resolve().parents[1]


def main():
    record("postprocess", "После обучения выполняются независимый инференс и визуальный отчёт", "hm_postprocess_v1", status="inference")
    failures = []
    for seed in selected_seeds():
        folder = ROOT / f"RelBenchGNN/results/seed_{seed}"
        if not (folder / "metrics.json").exists():
            raise RuntimeError(f"Training not complete: seed {seed}")
        check_path = folder / "inference/inference_check.json"
        if check_path.exists() and json.loads(check_path.read_text()).get("passed") and all((folder / f"inference/{split}_candidates.parquet").exists() for split in ["val", "test"]):
            continue
        with (ROOT / f"RelBenchGNN/logs/inference_seed_{seed}.log").open("w") as log:
            result = subprocess.run([sys.executable, "-u", str(ROOT / "RelBenchGNN/run_inference.py"),
                                     "--output_dir", str(folder)], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode != 0:
            failures.append(seed)
    if not failures:
        record("manual_baseline_queue", "После проверки ID-GNN запускаются дерево и LightGBM на ручных признаках", "hm_manual_tree_pipeline_v1", status="features")
        with (ROOT / "RelBenchGNN/logs/manual_tree.log").open("a") as log:
            result = subprocess.run([sys.executable, "-u", str(ROOT / "baseline/run_manual_tree.py")], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode != 0:
            failures.append("manual_tree_baseline")
    subprocess.run([sys.executable, str(ROOT / "RelBenchGNN/build_report.py")], cwd=ROOT, check=True)
    record("postprocess_complete", "Инференс и ручные baseline проверены, таблицы и графики сохранены" if not failures else "Отчёт сохранён; есть ошибки инференса или ручного baseline",
           "hm_postprocess_v1", status="complete" if not failures else "failed",
           failed_seeds=failures, artifacts="reports/relbench_hm_v1/report.md")
    if failures:
        raise RuntimeError(f"Inference failed for seeds: {failures}")


if __name__ == "__main__":
    main()
