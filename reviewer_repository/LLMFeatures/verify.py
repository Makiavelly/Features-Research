"""Independent replay on fixed 32-user subsets; not a full repeat evaluation."""
import hashlib
import json
from pathlib import Path
import sys

import lightgbm as lgb
import numpy as np

from features import FeatureEngine, ROOT
from evaluate import full_catalog, atomic_json, CACHE
from relbench import load_dataset


def main():
    directory = Path(sys.argv[1])
    program = json.loads((directory / "program.json").read_text())
    model = lgb.Booster(model_file=str(directory / "model.txt"))
    task = load_dataset(ROOT / "data/rel-hm").load_task("user-item-purchase")
    engine = FeatureEngine(CACHE / "verification")
    checks = {}
    for split in ["val", "test"]:
        table = task.get_table(split)
        rng = np.random.default_rng(42)
        indices = np.sort(rng.choice(len(table.df), min(32, len(table.df)), replace=False))
        table.df = table.df.iloc[indices].copy().reset_index(drop=True)
        predictions, seconds = full_catalog(engine, program, model, table, directory, split, "replay", resume=False)
        expected = np.load(directory / f"final_{split}_predictions.npy")[indices]
        checks[split] = {"users": len(indices), "reference_indices": indices.tolist(),
                         "catalog_size": len(engine.items), "predictions_identical": bool(np.array_equal(predictions, expected)),
                         "unique_ids": bool((np.diff(np.sort(predictions, axis=1), axis=1) != 0).all()),
                         "seconds": seconds}
    engine.close()
    result = {"passed": all(item["predictions_identical"] and item["unique_ids"] for item in checks.values()),
              "coverage": "32 fixed random users per split, complete catalog; not a full replay",
              "checks": checks, "model_sha256": hashlib.sha256((directory / "model.txt").read_bytes()).hexdigest()}
    atomic_json(directory / "verification.json", result)
    if not result["passed"]:
        raise RuntimeError("Independent inference replay mismatch")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
