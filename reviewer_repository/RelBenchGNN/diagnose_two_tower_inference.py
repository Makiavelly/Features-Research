"""Compare cached independent encodings without changing previous results."""
import json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
folder = ROOT / "RelBenchGNN/results/two_tower_seed_42"
report = {}
for split in ["val", "test"]:
    report[split] = {}
    for kind in ["user", "item"]:
        original = np.load(folder / f"embeddings/{split}_{kind}_embeddings.npy")
        repeated = np.load(folder / f"inference/{split}_{kind}_embeddings.npy")
        difference = np.abs(original-repeated)
        report[split][kind] = {"shape": list(original.shape), "identical": bool(np.array_equal(original, repeated)),
            "max_absolute_difference": float(difference.max()),
            "mean_absolute_difference": float(difference.mean()),
            "different_rows": int(np.any(original != repeated, axis=1).sum())}
print(json.dumps(report, indent=2), flush=True)
(folder / "inference/embedding_diagnostics.json").write_text(json.dumps(report, indent=2))
