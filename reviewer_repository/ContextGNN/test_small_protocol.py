"""Validate objective compatibility and subset temporal/key contracts."""
import torch
import numpy as np
import pandas as pd
import hashlib
import json
from run_small import sparse_ce, ROOT
from relbench import load_dataset
x = torch.randn(3, 5, requires_grad=True)
src, dst = torch.tensor([0, 0, 1, 2]), torch.tensor([1, 3, 0, 4])
y = torch.zeros_like(x)
y[src, dst] = 1
sparse = sparse_ce(x, src, dst)
dense = -(y*x.log_softmax(dim=-1)).sum()/len(x)
assert torch.allclose(sparse, dense)
assert torch.allclose(torch.autograd.grad(sparse, x, retain_graph=True)[0], torch.autograd.grad(dense, x)[0])
dataset = load_dataset(ROOT / "data/rel-hm-small-v1")
subset_root = ROOT / "data/rel-hm-small-v1"
manifest = json.loads((subset_root / "subset_manifest.json").read_text())
for name, metadata in manifest["files"].items():
    path = subset_root / name
    assert path.stat().st_size == metadata["bytes"]
    with path.open("rb") as file:
        assert hashlib.file_digest(file, "sha256").hexdigest() == metadata["sha256"]
task = dataset.load_task("user-item-purchase")
db = dataset.get_db()
for name in ["customer", "article"]:
    table = db.table_dict[name]
    assert np.array_equal(table.df[table.pkey_col], np.arange(5000))
tx = db.table_dict["transactions"].df
assert len(tx) == 46442
assert tx.customer_id.between(0,4999).all() and tx.article_id.between(0,4999).all()
assert tx.t_dat.max() <= pd.Timestamp("2020-09-14")
train = task.get_table("train").df
assert (train.timestamp+pd.Timedelta(days=7) <= dataset.val_timestamp).all()
for split in ["train", "val", "test"]:
    frame = task.get_table(split, mask_input_cols=False).df
    assert not frame.duplicated(["customer_id", "timestamp"]).any()
    assert all(len(items)>0 and np.min(items)>=0 and np.max(items)<5000 for items in frame.article_id)
print("PASS: sparse CE value/gradient; subset FK, ID, labels and temporal split contracts", flush=True)
