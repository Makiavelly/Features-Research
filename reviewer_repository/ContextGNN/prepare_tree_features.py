"""Shared sampled train pairs and full-catalog manual features on the pilot."""
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from relbench import load_dataset
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "baseline"), str(ROOT / "RelBenchGNN")]
from manual_features import ManualFeatures
from tracking import record
CACHE = ROOT / "ContextGNN/cache/hm_small_v1/manual"
CACHE.mkdir(parents=True, exist_ok=True)
manifest_file = CACHE / "manifest.json"
if manifest_file.exists():
    raise SystemExit(0)
task = load_dataset(ROOT / "data/rel-hm-small-v1").load_task("user-item-purchase")
engine = ManualFeatures(data_dir=ROOT / "data/rel-hm-small-v1/db", cache_dir=CACHE)
rng = np.random.default_rng(2026)
files = {split: [] for split in ["train", "val", "test"]}
train_rows = 0
for index, (timestamp, group) in enumerate(task.get_table("train").df.groupby("timestamp", sort=True)):
    engine.prepare(timestamp, group.customer_id.values)
    history = engine.history_candidates().set_index("customer_id").candidates.to_dict()
    rows = []
    for row in group.itertuples():
        positive = set(int(item) for item in row.article_id)
        past = np.array(sorted(set(history.get(row.customer_id, []))-positive), dtype=np.int64)
        hard = rng.choice(past, min(8, len(past)), replace=False) if len(past) else []
        negative = set(map(int, hard))
        while len(negative) < len(hard)+8:
            item = int(rng.integers(5000))
            if item not in positive:
                negative.add(item)
        rows.extend((row.customer_id, item, 1) for item in sorted(positive))
        rows.extend((row.customer_id, item, 0) for item in sorted(negative))
    frame = pd.DataFrame(rows, columns=["customer_id", "article_id", "label"])
    path = CACHE / f"train_{index}.parquet"
    engine.write(frame, path)
    train_rows += len(frame)
    files["train"].append(str(path.relative_to(ROOT)))
for split in ["val", "test"]:
    table = task.get_table(split)
    engine.prepare(table.df.timestamp.iloc[0], table.df.customer_id.values)
    candidates = pd.DataFrame({"customer_id": table.df.customer_id.values,
                               "candidates": [np.arange(5000, dtype=np.int64)]*len(table.df)})
    candidates.to_parquet(CACHE / f"{split}_candidates.parquet", index=False)
    for part, start in enumerate(range(0, len(candidates), 16)):
        users = candidates.customer_id.values[start:start+16]
        pairs = pd.DataFrame({"customer_id": np.repeat(users, 5000), "article_id": np.tile(np.arange(5000), len(users))})
        path = CACHE / f"{split}_{part}.parquet"
        engine.write(pairs, path)
        files[split].append(str(path.relative_to(ROOT)))
    record("small_manual_features", f"Ручные признаки {split} готовы: {len(table.df)} пользователей ×5000 товаров", "hm_small_manual_features_v1", status="features", split=split, pairs=len(table.df)*5000)
engine.save_schema(CACHE / "schema.json")
engine.close()
manifest_file.write_text(json.dumps({"files": files, "train_pairs": train_rows, "train_user_times": 4804,
    "catalog": 5000, "negative_sampling": "up to8history+8uniform, seed2026; all positives", "evaluation": "full subset catalog"}, indent=2))
record("small_manual_features_complete", "Общие обучающие пары двух LightGBM и ручные признаки малого набора сохранены", "hm_small_manual_features_v1", status="complete", train_pairs=train_rows, artifacts=str(CACHE.relative_to(ROOT)))
