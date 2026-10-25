import json
from pathlib import Path
import statistics
import subprocess
import sys
from tracking import record
from experiment_plan import selected_seeds

ROOT = Path(__file__).resolve().parents[1]
SEEDS = selected_seeds()
records = [json.loads(p.read_text()) for seed in SEEDS if (p := ROOT / f"RelBenchGNN/results/seed_{seed}/metrics.json").exists()]
summary = {"completed_runs": len(records), "expected_runs": len(SEEDS), "selected_seeds": SEEDS, "runs": records,
           "published_map_percent": {"val": 2.64, "test": 2.81},
           "published_std_percent": {"val": 0.00, "test": 0.01}}
for split in ["val", "test"]:
    values = [r[f"{split}_metrics"]["map"] * 100 for r in records]
    if values:
        summary[split] = {"mean_map_percent": statistics.mean(values),
                          "std_map_percent": statistics.pstdev(values) if len(values) > 1 else None,
                          "difference_from_paper_pp": statistics.mean(values) - summary["published_map_percent"][split]}
target = ROOT / "RelBenchGNN/results/summary.json"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(summary, indent=2))
record("summary", "Обновлена сводка завершённых прогонов ID-GNN", "hm_idgnn_last_summary_v1",
       status="complete" if len(records) == len(SEEDS) else "partial", completed_runs=len(records), expected_runs=len(SEEDS),
       val_metrics={"map": summary["val"]["mean_map_percent"] / 100} if records else {},
       test_metrics={"map": summary["test"]["mean_map_percent"] / 100} if records else {},
       artifacts="RelBenchGNN/results/summary.json")
print(json.dumps(summary, indent=2))
if len(records) == len(SEEDS) and "--summary-only" not in sys.argv:
    subprocess.run([sys.executable, str(ROOT / "RelBenchGNN/postprocess.py")], check=True)
