"""Persist a train-selected, reindexed H&M pilot without changing the source."""
from pathlib import Path
import json
import hashlib
import shutil
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import duckdb
import yaml
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "RelBenchGNN"))
from tracking import record
SOURCE = ROOT / "data/rel-hm"
OUT = ROOT / "data/rel-hm-small-v1"
if (OUT / "subset_manifest.json").exists():
    print((OUT / "subset_manifest.json").read_text(), flush=True)
    raise SystemExit(0)
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "db").mkdir(exist_ok=True)
task_out = OUT / "tasks/user-item-purchase"
task_out.mkdir(parents=True, exist_ok=True)
record("small_data_start", "Создание отдельного малого H&M: до5000 пользователей/товаров, выбор только по прошлой истории", "hm_small_data_v1", status="preparing")
val_time, test_time = pd.Timestamp("2020-09-07"), pd.Timestamp("2020-09-14")
history_start = val_time - pd.Timedelta(days=180)
con = duckdb.connect()
con.sql("SET threads=2")
con.sql("SET memory_limit='1GB'")
tx_file = str(SOURCE / "db/transactions.parquet")
eligible = con.execute("SELECT DISTINCT customer_id FROM read_parquet(?) WHERE t_dat >= ? AND t_dat <= ? ORDER BY customer_id", [tx_file, val_time-pd.Timedelta(days=90), val_time]).fetchnumpy()["customer_id"]
users = np.sort(np.random.default_rng(42).choice(eligible, min(5000, len(eligible)), replace=False))
user_map = pd.DataFrame({"original_customer_id": users, "customer_id": np.arange(len(users), dtype=np.int64)})
con.register("chosen_users", user_map)
items = con.execute("""SELECT t.article_id AS original_article_id, count(*) AS historical_count
    FROM read_parquet(?) t JOIN chosen_users u ON t.customer_id=u.original_customer_id
    WHERE t_dat >= ? AND t_dat <= ? GROUP BY t.article_id
    ORDER BY historical_count DESC, original_article_id ASC LIMIT 5000""", [tx_file, history_start, val_time]).fetchdf().sort_values("original_article_id").reset_index(drop=True)
items["article_id"] = np.arange(len(items), dtype=np.int64)
con.register("chosen_items", items)
tx = con.execute("""SELECT t.* EXCLUDE(customer_id,article_id), u.customer_id, a.article_id
    FROM read_parquet(?) t JOIN chosen_users u ON t.customer_id=u.original_customer_id
    JOIN chosen_items a ON t.article_id=a.original_article_id
    WHERE t_dat >= ? AND t_dat <= ? ORDER BY t_dat, u.customer_id, a.article_id""", [tx_file, history_start, test_time]).fetchdf()
assert len(tx) <= 200000, "Pilot graph exceeds declared transaction budget"
pq.write_table(pa.Table.from_pandas(tx, preserve_index=False), OUT / "db/transactions.parquet", compression="zstd")
for table, old_ids, id_column in [("customer", users, "customer_id"), ("article", items.original_article_id.to_numpy(), "article_id")]:
    frame = pq.read_table(SOURCE / f"db/{table}.parquet", filters=[(id_column, "in", old_ids.tolist())]).to_pandas().sort_values(id_column).reset_index(drop=True)
    assert np.array_equal(frame[id_column].values, old_ids)
    frame[id_column] = np.arange(len(frame), dtype=np.int64)
    pq.write_table(pa.Table.from_pandas(frame, preserve_index=False), OUT / f"db/{table}.parquet", compression="zstd")
user_map.to_csv(OUT / "customer_id_map.csv", index=False)
items.to_csv(OUT / "article_id_map.csv", index=False)
manifest = yaml.safe_load((SOURCE / "manifest.yaml").read_text())
manifest["name"] = "rel-hm-small-v1"
(OUT / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False))
shutil.copyfile(SOURCE / "tasks/user-item-purchase/manifest.yaml", task_out / "manifest.yaml")
item_lookup = dict(zip(items.original_article_id, items.article_id))
user_lookup = dict(zip(user_map.original_customer_id, user_map.customer_id))
stats = {}
training_times = None
for split in ["train", "val", "test"]:
    frame = pq.read_table(SOURCE / f"tasks/user-item-purchase/{split}.parquet", filters=[("customer_id", "in", users.tolist())]).to_pandas()
    if split == "train":
        training_times = sorted(frame.timestamp.unique())[-8:]
        frame = frame[frame.timestamp.isin(training_times)].copy()
    original_rows = len(frame)
    original_positives = int(frame.article_id.map(len).sum())
    frame["article_id"] = frame.article_id.map(lambda values: np.asarray(sorted({item_lookup[int(item)] for item in values if int(item) in item_lookup}), dtype=np.int64))
    retained_positives = int(frame.article_id.map(len).sum())
    frame = frame[frame.article_id.map(len) > 0].copy()
    frame["customer_id"] = frame.customer_id.map(user_lookup).astype(np.int64)
    frame = frame.reset_index(drop=True)
    assert len(frame) > 0
    pq.write_table(pa.Table.from_pandas(frame, preserve_index=False), task_out / f"{split}.parquet", compression="zstd")
    stats[split] = {"source_cohort_rows": original_rows, "retained_rows": len(frame), "original_positive_items": original_positives,
        "retained_positive_items": retained_positives, "positive_coverage": retained_positives/original_positives,
        "dropped_empty_rows": original_rows-len(frame), "min_timestamp": str(frame.timestamp.min()), "max_timestamp": str(frame.timestamp.max())}
files = {}
for path in sorted(OUT.rglob("*")):
    if path.is_file():
        with path.open("rb") as file:
            files[str(path.relative_to(OUT))] = {"bytes": path.stat().st_size, "sha256": hashlib.file_digest(file, "sha256").hexdigest()}
summary = {"source": "data/rel-hm", "seed": 42, "users": len(users), "items": len(items), "transactions": len(tx),
    "history_start": str(history_start), "val_time": str(val_time), "test_time": str(test_time),
    "selection": "users active during 90 days before validation; uniform seed42; top5000 items by 180day pre-validation cohort counts; last8 train timestamps; no val/test labels used for membership",
    "protocol_caveat": "restricted catalog and removal of empty-label rows change task; MAP cannot be compared directly with full H&M/paper",
    "splits": stats, "files": files}
(OUT / "subset_manifest.json").write_text(json.dumps(summary, indent=2))
record("small_data_complete", "Малый H&M сохранён отдельно, ключи перенумерованы, покрытие будущих целей измерено после фиксации состава", "hm_small_data_v1", status="complete", config=summary, artifacts=str(OUT.relative_to(ROOT)))
print(json.dumps(summary, indent=2), flush=True)
