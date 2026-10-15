"""Check replay allowing only numerically indistinguishable score ties."""
import numpy as np


def verify_replay(folder, split, pred, expected, metrics, reference):
    shape_ok = pred.shape == expected.shape
    unique = bool((np.diff(np.sort(pred, axis=1), axis=1) != 0).all())
    original_users = np.load(folder / f"embeddings/{split}_user_embeddings.npy")
    original_items = np.load(folder / f"embeddings/{split}_item_embeddings.npy")
    users = np.load(folder / f"inference/{split}_user_embeddings.npy")
    items = np.load(folder / f"inference/{split}_item_embeddings.npy")
    embedding_atol, embedding_rtol = 1e-6, 1e-6
    embeddings_close = all(np.allclose(old, new, atol=embedding_atol, rtol=embedding_rtol)
                           for old, new in [(original_users, users), (original_items, items)])
    ids_valid = bool(((pred >= 0) & (pred < len(items))).all())
    max_score_difference = 0.0
    score_ties_close = shape_ok and ids_valid
    if score_ties_close:
        for start in range(0, len(pred), 2048):
            stop = min(start+2048, len(pred))
            # Compare rank-by-rank scores under the SAME repeated embeddings.
            # Different IDs pass only when their scores are numerical ties.
            user_vectors = users[start:stop, None, :].astype(np.float64)
            actual_scores = (user_vectors * items[pred[start:stop]].astype(np.float64)).sum(axis=2)
            original_scores = (user_vectors * items[expected[start:stop]].astype(np.float64)).sum(axis=2)
            max_score_difference = max(max_score_difference, float(np.abs(actual_scores-original_scores).max()))
            score_ties_close &= bool(np.allclose(actual_scores, original_scores, atol=1e-5, rtol=1e-6))
    map_difference = abs(metrics["map"] - reference[f"{split}_metrics"]["map"])
    return {"verification_protocol": "numerical_ties_v2", "shape_ok": shape_ok,
            "unique_ids": unique, "ids_valid": ids_valid,
            "predictions_identical": bool(np.array_equal(pred, expected)),
            "same_item_at_same_rank_fraction": float((pred == expected).mean()) if shape_ok else 0.,
            "embeddings_close": bool(embeddings_close), "embedding_atol": embedding_atol,
            "embedding_rtol": embedding_rtol,
            "max_embedding_absolute_difference": max(float(np.abs(users-original_users).max()), float(np.abs(items-original_items).max())),
            "ranked_scores_close": bool(score_ties_close), "score_atol": 1e-5, "score_rtol": 1e-6,
            "max_ranked_score_absolute_difference": max_score_difference,
            "map_absolute_difference": map_difference, "map_tolerance": 1e-6,
            "passed": bool(shape_ok and unique and ids_valid and embeddings_close and score_ties_close and map_difference <= 1e-6)}
