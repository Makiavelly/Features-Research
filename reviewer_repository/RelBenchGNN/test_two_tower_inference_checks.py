"""Ensure tie-aware verification rejects substantive differences."""
import tempfile
from pathlib import Path
import numpy as np
from two_tower_inference_checks import verify_replay

with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    (root / "embeddings").mkdir()
    (root / "inference").mkdir()
    users = np.ones((2, 2), dtype=np.float32)
    items = np.ones((14, 2), dtype=np.float32)
    def save():
        for target in ["embeddings", "inference"]:
            np.save(root / f"{target}/val_user_embeddings.npy", users)
            np.save(root / f"{target}/val_item_embeddings.npy", items)
    save()
    original = np.tile(np.arange(12), (2, 1))
    tied = np.tile(np.arange(1, 13), (2, 1))
    reference = {"val_metrics": {"map": .1}}
    assert verify_replay(root, "val", original, original, {"map": .1}, reference)["passed"]
    assert verify_replay(root, "val", tied, original, {"map": .1}, reference)["passed"]
    assert not verify_replay(root, "val", tied, original, {"map": .2}, reference)["passed"]
    items[12] = 20
    save()
    assert not verify_replay(root, "val", tied, original, {"map": .1}, reference)["passed"]
    users *= 2
    np.save(root / "inference/val_user_embeddings.npy", users)
    assert not verify_replay(root, "val", original, original, {"map": .1}, reference)["passed"]
print("PASS: exact replay/ties accepted; score, embedding and MAP drift rejected")
