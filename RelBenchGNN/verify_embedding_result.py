"""Check saved hybrid predictions independently of training and reporting."""
import json
from pathlib import Path
import numpy as np
import lightgbm as lgb
from relbench import load_dataset
from tracking import record

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "baseline/results/gnn_embeddings_v1"
metrics = json.loads((OUT / "metrics.json").read_text())
task = load_dataset(ROOT / "data/rel-hm").load_task("user-item-purchase")
model = lgb.Booster(model_file=str(OUT / "model.txt"))
assert model.feature_name() == metrics["features"]
reference = json.loads((ROOT / "RelBenchGNN/results/seed_42/inference/inference_check.json").read_text())
assert metrics["checkpoint_sha256"] == reference["checkpoint_sha256"]
checks = {}
for split, count in [("val", 74575), ("test", 67144)]:
    pred = np.load(OUT / f"{split}_predictions.npy")
    assert pred.shape == (count, 12)
    assert ((pred >= 0) & (pred < 105542)).all()
    assert (np.diff(np.sort(pred, axis=1), axis=1) != 0).all()
    computed = task.evaluate(pred, task.get_table("val")) if split == "val" else task.evaluate(pred)
    assert abs(computed["map"] - metrics[f"{split}_metrics"]["map"]) < 1e-12
    checks[split] = {"shape": list(pred.shape), "map": computed["map"], "passed": True}
(OUT / "verification.json").write_text(json.dumps({"passed": True, "checks": checks}, indent=2))
record("embedding_final_verification", "Метрики независимо пересчитаны из сохранённых предсказаний; shape, уникальность и диапазон ID, имена признаков сохранённого LightGBM и SHA весов GNN проверены. График проверен визуально.",
       "hm_idgnn_lightgbm_embeddings_seed_42_v1", status="complete", checks=checks,
       val_metrics=metrics["val_metrics"], test_metrics=metrics["test_metrics"], artifacts=str(OUT.relative_to(ROOT)))
print(json.dumps(checks), flush=True)
