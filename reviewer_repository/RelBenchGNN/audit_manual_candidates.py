"""Audit saved manual predictions and cached pair sets against ID-GNN pools."""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow.dataset as pads
from relbench import load_dataset
from tracking import record

ROOT = Path(__file__).resolve().parents[1]
task = load_dataset(ROOT / "data/rel-hm").load_task("user-item-purchase")
build = json.loads((ROOT / "baseline/cache/manual_v1/build_complete.json").read_text())
checks = {}
for split in ["val", "test"]:
    path = ROOT / f"RelBenchGNN/results/seed_42/inference/{split}_candidates.parquet"
    frame = pd.read_parquet(path)
    users = task.get_table(split).df.customer_id.to_numpy(dtype=np.int64)
    assert np.array_equal(users, frame.customer_id.values)
    counts = frame.candidates.map(len).to_numpy()
    keys = np.repeat(users, counts) * 1_000_000 + np.concatenate(frame.candidates.values)
    keys.sort()
    assert len(np.unique(keys)) == len(keys)
    pairs = pads.dataset([str(ROOT / name) for name in build["files"][split]], format="parquet").to_table(columns=["customer_id", "article_id"]).to_pandas()
    cached_keys = pairs.customer_id.to_numpy(dtype=np.int64) * 1_000_000 + pairs.article_id.to_numpy(dtype=np.int64)
    cached_keys.sort()
    assert np.array_equal(keys, cached_keys)
    methods = {}
    for name, prediction_path in [
        ("idgnn", ROOT / f"RelBenchGNN/results/seed_42/{split}_predictions.npy"),
        ("lightgbm_manual", ROOT / f"baseline/results/manual_v1/lightgbm/seed_42/{split}_predictions.npy"),
        ("decision_tree_manual", ROOT / f"baseline/results/manual_v1/decision_tree/seed_42/{split}_predictions.npy")]:
        pred = np.load(prediction_path)
        assert pred.shape == (len(users), 12)
        predicted_keys = (users[:, None]*1_000_000 + pred).ravel()
        positions = np.searchsorted(keys, predicted_keys)
        included = (positions < len(keys)) & (keys[np.minimum(positions, len(keys)-1)] == predicted_keys)
        assert included.all(), (split, name, int((~included).sum()))
        methods[name] = {"recommendations": pred.size, "outside_pool": int((~included).sum())}
    with path.open("rb") as file:
        digest = hashlib.file_digest(file, "sha256").hexdigest()
    checks[split] = {"users": len(users), "candidate_pairs": len(keys), "mean_candidates": float(counts.mean()),
                     "feature_pairs_exactly_match_pool": True, "candidate_file_sha256": digest, "methods": methods}
result = {"passed": True, "seed": 42, "checks": checks,
          "scope": "manual_v1 vs ID-GNN; pool is sampled item IDs union original ID-GNN top12 (including zero-score fallbacks); not full catalog for manual models"}
target = ROOT / "reports/relbench_hm_v1/candidate_audit.json"
target.write_text(json.dumps(result, indent=2))
record("candidate_pool_audit", "По запросу пользователя проверены фактические candidate pools: пары val/test ручных признаков точно совпадают с экспортом ID-GNN seed42; все top12 ID-GNN/LightGBM manual/DecisionTree manual внутри того же pool. Важное уточнение: ID-GNN вычисляет sigmoid для sampled товаров и ноль остальному каталогу; экспорт добавляет zero-score fallback top12.", checks=checks, artifacts=str(target.relative_to(ROOT)))
print(json.dumps(result, indent=2), flush=True)
