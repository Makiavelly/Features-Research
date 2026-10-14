"""CPU decision-tree and LightGBM baselines on explicit historical features."""
import argparse
import gc
import json
from pathlib import Path
import sys
import time

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd
import pyarrow.dataset as pads
import pyarrow.parquet as pq
from scipy import sparse
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from relbench import load_dataset

from manual_features import ManualFeatures, ROOT
sys.path.insert(0, str(ROOT / "RelBenchGNN"))
from tracking import record
from experiment_plan import selected_seeds
SEEDS = selected_seeds()

OUT = ROOT / "baseline/results/manual_v1"
CACHE = ROOT / "baseline/cache/manual_v1"
RUN_ID = "hm_manual_tree_pipeline_v1"


def check_candidates(folder):
    """Use exactly the candidates sampled/scored by ID-GNN, without target labels."""
    result = {}
    for split in ["val", "test"]:
        frames = []
        for seed in SEEDS:
            file = ROOT / f"RelBenchGNN/results/seed_{seed}/inference/{split}_candidates.parquet"
            frame = pd.read_parquet(file)
            frames.append(frame)
        for frame in frames[1:]:
            if not np.array_equal(frames[0].customer_id.values, frame.customer_id.values):
                raise RuntimeError("Candidate user order differs between GNN seeds")
        combined = frames[0].copy()
        combined["candidates"] = [np.unique(np.concatenate(items)) for items in zip(*(frame.candidates for frame in frames))]
        result[split] = combined
    return result


def build_features(task, train_user_times):
    CACHE.mkdir(parents=True, exist_ok=True)
    manifest_file = CACHE / "feature_manifest.json"
    build_file = CACHE / "build_complete.json"
    if build_file.exists():
        build = json.loads(build_file.read_text())
        if build["train_user_times"] != train_user_times:
            raise RuntimeError("Changed training budget requires a new experiment/cache directory")
        return json.loads(manifest_file.read_text()), build
    shared = check_candidates(CACHE)
    engine = ManualFeatures()
    rng = np.random.default_rng(2026)
    labels = task.get_table("train").df
    selected = np.sort(rng.choice(len(labels), min(train_user_times, len(labels)), replace=False))
    sampled = labels.iloc[selected].copy()
    catalog = np.arange(engine.con.sql("SELECT count(*) FROM articles").fetchone()[0])
    files = {"train": [], "val": [], "test": []}
    groups = list(sampled.groupby("timestamp", sort=True))
    for number, (timestamp, frame) in enumerate(groups):
        record("feature_snapshot", f"Ручные признаки train: дата {timestamp.date()}, {number+1}/{len(groups)}", RUN_ID, status="features")
        engine.prepare(timestamp, frame.customer_id.values)
        lookup = engine.history_candidates().set_index("customer_id").candidates.to_dict()
        pairs = []
        for user, positives in zip(frame.customer_id.values, frame.article_id.values):
            true = set(int(i) for i in positives)
            hard = np.array(sorted(set(int(i) for i in lookup.get(user, [])) - true), dtype=np.int64)
            hard = rng.choice(hard, min(8, len(hard)), replace=False) if len(hard) else []
            negative = set(int(i) for i in hard)
            while len(negative) < len(hard) + 8:
                item = int(rng.choice(catalog))
                if item not in true:
                    negative.add(item)
            pairs.extend((int(user), item, 1) for item in sorted(true))
            pairs.extend((int(user), item, 0) for item in sorted(negative))
        pairs = pd.DataFrame(pairs, columns=["customer_id", "article_id", "label"])
        file = CACHE / "features/train" / f"snapshot_{number:02d}.parquet"
        engine.write(pairs, file)
        files["train"].append(str(file.relative_to(ROOT)))
    candidate_stats = {}
    for split, frame in shared.items():
        timestamp = frame.timestamp.iloc[0]
        engine.prepare(timestamp, frame.customer_id.values)
        target = task.get_table(split, mask_input_cols=split == "test")
        if not np.array_equal(target.df.customer_id.values, frame.customer_id.values):
            raise RuntimeError("Candidates not aligned to task evaluation rows")
        candidate_stats[split] = {"mean_candidate_count_union": float(frame.candidates.map(len).mean())}
        if split == "val":
            hits = np.array([len(np.intersect1d(candidates, true)) for candidates, true in zip(frame.candidates, target.df.article_id)])
            sizes = target.df.article_id.map(len).values
            candidate_stats[split].update({"users_with_relevant_candidate_fraction_union": float((hits > 0).mean()),
                                          "candidate_recall_union": float((hits / sizes).mean()),
                                          "oracle_map_upper_bound_union": float((np.minimum(hits, task.eval_k) / np.minimum(sizes, task.eval_k)).mean())})
        for part, start in enumerate(range(0, len(frame), 5000)):
            small = frame.iloc[start:start+5000]
            pairs = small[["customer_id", "candidates"]].explode("candidates").rename(columns={"candidates": "article_id"})
            pairs.article_id = pairs.article_id.astype(np.int64)
            file = CACHE / f"features/{split}" / f"part_{part:02d}.parquet"
            engine.write(pairs, file)
            files[split].append(str(file.relative_to(ROOT)))
        record("feature_snapshot", f"Ручные признаки полного {split} сохранены", RUN_ID, status="features", candidate_stats=candidate_stats[split])
    engine.save_schema(manifest_file)
    engine.close()
    build = {"train_user_times": len(sampled), "negative_sampling_seed": 2026,
             "negative_sampling": "up to 8 history negatives + 8 uniform catalog negatives; exclude all positives",
             "files": files, "candidate_stats": candidate_stats,
             "shared_candidates": "each tree seed is evaluated on the exact respective ID-GNN inference pool; cached features use their union"}
    build_file.write_text(json.dumps(build, indent=2))
    return json.loads(manifest_file.read_text()), build


def dense(frame, features):
    values = frame[features].to_numpy(dtype=np.float32)
    return np.nan_to_num(values, nan=-1., posinf=-1., neginf=-1.)


class TreeEncoding:
    def __init__(self, features, categorical):
        self.categorical = [features.index(c) for c in categorical]
        self.numerical = [i for i in range(len(features)) if i not in self.categorical]
        self.encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=True, dtype=np.float32)

    def fit(self, values):
        self.encoder.fit(values[:, self.categorical])
        return self

    def transform(self, values):
        return sparse.hstack([sparse.csr_matrix(values[:, self.numerical]), self.encoder.transform(values[:, self.categorical])], format="csr", dtype=np.float32)


def predict(model, encoding, files, features, target, k=12, seed=42, split="val", candidate_file=None):
    """Streaming top-k: bounded memory even for millions of candidate pairs."""
    user_ids = target.df.customer_id.to_numpy(dtype=np.int64)
    lookup = np.full(user_ids.max() + 1, -1, dtype=np.int32)
    lookup[user_ids] = np.arange(len(user_ids))
    candidate_file = candidate_file or ROOT / f"RelBenchGNN/results/seed_{seed}/inference/{split}_candidates.parquet"
    allowed = pd.read_parquet(candidate_file)
    allowed = allowed[allowed.customer_id.isin(user_ids)]
    counts = allowed.candidates.map(len).values
    allowed_keys = np.repeat(allowed.customer_id.values, counts) * 1_000_000 + np.concatenate(allowed.candidates.values).astype(np.int64)
    allowed_keys.sort()
    del allowed
    scores = np.full((len(user_ids), k), -np.inf, dtype=np.float64)
    items = np.full((len(user_ids), k), -1, dtype=np.int64)
    dataset = pads.dataset([str(ROOT / file) for file in files], format="parquet")
    scanner = dataset.scanner(columns=["customer_id", "article_id", *features], filter=pads.field("customer_id").isin(user_ids), batch_size=50000)
    start = time.perf_counter()
    for batch in scanner.to_batches():
        frame = batch.to_pandas()
        keys = frame.customer_id.values * 1_000_000 + frame.article_id.values
        positions = np.searchsorted(allowed_keys, keys)
        keep = (positions < len(allowed_keys)) & (allowed_keys[np.minimum(positions, len(allowed_keys)-1)] == keys)
        frame = frame.loc[keep]
        if frame.empty:
            continue
        values = dense(frame, features)
        if encoding is not None:
            values = encoding.transform(values)
            probabilities = model.predict_proba(values)[:, 1]
        else:
            probabilities = model.predict(values, num_threads=2)
        if not np.isfinite(probabilities).all():
            raise RuntimeError("Non-finite tree probabilities")
        indices = lookup[frame.customer_id.values]
        order = np.argsort(indices, kind="stable")
        ordered = indices[order]
        boundaries = np.r_[0, np.flatnonzero(np.diff(ordered)) + 1, len(order)]
        candidate_ids = frame.article_id.to_numpy(dtype=np.int64)
        for left, right in zip(boundaries[:-1], boundaries[1:]):
            index = ordered[left]
            selection = order[left:right]
            existing = items[index] >= 0
            joined_ids = np.r_[items[index, existing], candidate_ids[selection]]
            joined_scores = np.r_[scores[index, existing], probabilities[selection]]
            best = np.lexsort((joined_ids, -joined_scores))[:k]
            items[index] = -1
            scores[index] = -np.inf
            items[index, :len(best)] = joined_ids[best]
            scores[index, :len(best)] = joined_scores[best]
    if (items < 0).any() or (np.diff(np.sort(items, axis=1), axis=1) == 0).any():
        raise RuntimeError("Invalid or repeated top-k IDs")
    return items, time.perf_counter() - start


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-user-times", type=int, default=50000)
    parser.add_argument("--tune-users", type=int, default=10000)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    record("manual_baseline_start", "Начато построение и обучение дерева и LightGBM на ручных признаках", RUN_ID, status="features", config=vars(args))
    dataset = load_dataset(ROOT / "data/rel-hm")
    task = dataset.load_task("user-item-purchase")
    schema, build = build_features(task, args.train_user_times)
    features = schema["features"]
    train_files = [ROOT / file for file in build["files"]["train"]]
    train = pads.dataset(train_files, format="parquet").to_table(columns=["label", *features]).to_pandas()
    values = dense(train, features)
    labels = train.label.to_numpy(dtype=np.int8)
    del train
    gc.collect()
    val = task.get_table("val")
    tuning = task.get_table("val")
    rng = np.random.default_rng(2026)
    tuning.df = tuning.df.iloc[np.sort(rng.choice(len(tuning), min(args.tune_users, len(tuning)), replace=False))].copy()
    encoding = TreeEncoding(features, schema["categorical_features"]).fit(values)
    encoded = encoding.transform(values)
    trials = []
    best_depth, best_metric = None, -1
    for depth in [8, 12, 16]:
        model = DecisionTreeClassifier(max_depth=depth, min_samples_leaf=100, class_weight="balanced", random_state=42)
        model.fit(encoded, labels)
        predictions, _ = predict(model, encoding, build["files"]["val"], features, tuning)
        metric = task.evaluate(predictions, tuning)["map"]
        trials.append({"model": "DecisionTree", "max_depth": depth, "validation_tuning_map": metric})
        if metric > best_metric:
            best_depth, best_metric = depth, metric
    del model, encoded
    gc.collect()
    categorical_indices = [features.index(c) for c in schema["categorical_features"]]
    parameters = {"objective": "binary", "verbosity": -1, "num_threads": 2, "learning_rate": .05,
                  "min_data_in_leaf": 100, "max_bin": 127, "feature_fraction": .9, "bagging_fraction": .8,
                  "bagging_freq": 1, "deterministic": True, "force_col_wise": True, "seed": 42}
    train_dataset = lgb.Dataset(values, label=labels, feature_name=features, categorical_feature=categorical_indices, free_raw_data=False)
    best_leaves, best_metric = None, -1
    for leaves in [15, 31]:
        model = lgb.train({**parameters, "num_leaves": leaves}, train_dataset, num_boost_round=150)
        predictions, _ = predict(model, None, build["files"]["val"], features, tuning)
        metric = task.evaluate(predictions, tuning)["map"]
        trials.append({"model": "LightGBM", "num_leaves": leaves, "validation_tuning_map": metric})
        if metric > best_metric:
            best_leaves, best_metric = leaves, metric
    config = {"adapted_expert_features": True, "feature_count": len(features), "train_user_times": build["train_user_times"],
              "train_pairs": len(labels), "tuning_validation_users": len(tuning), "decision_tree_depth": best_depth,
              "decision_tree_min_leaf": 100, "lightgbm_num_leaves": best_leaves, "lightgbm_rounds": 150,
              "lightgbm_parameters": parameters, "trials": trials,
              "shared_candidates": build["shared_candidates"], "candidate_stats": build["candidate_stats"],
              "ties": "descending predicted score, ascending article_id; no target-dependent tie breaking"}
    (OUT / "config.json").write_text(json.dumps(config, indent=2))
    record("manual_baseline_tuned", "Параметры выбраны только по validation; тест не использован для подбора", RUN_ID, status="training", config=config)
    test = task.get_table("test", mask_input_cols=False)
    for kind in ["decision_tree", "lightgbm"]:
        for seed in SEEDS:
            folder = OUT / f"{kind}/seed_{seed}"
            folder.mkdir(parents=True, exist_ok=True)
            if (folder / "metrics.json").exists():
                continue
            run_id = f"hm_{kind}_manual_seed_{seed}_v1"
            record("manual_model_start", f"Обучение {kind} на ручных признаках, seed {seed}", run_id, status="training", config=config)
            if kind == "decision_tree":
                encoded = encoding.transform(values)
                model = DecisionTreeClassifier(max_depth=best_depth, min_samples_leaf=100, class_weight="balanced", random_state=seed).fit(encoded, labels)
                del encoded
                joblib.dump({"model": model, "onehot_encoder": encoding.encoder, "numerical_columns": encoding.numerical,
                             "categorical_columns": encoding.categorical, "features": features}, folder / "model.joblib")
                loaded = joblib.load(folder / "model.joblib")
                model, active_encoding = loaded["model"], encoding
                active_encoding.encoder = loaded["onehot_encoder"]
            else:
                model = lgb.train({**parameters, "num_leaves": best_leaves, "seed": seed}, train_dataset, num_boost_round=150)
                model.save_model(str(folder / "model.txt"))
                model = lgb.Booster(model_file=str(folder / "model.txt"))
                active_encoding = None
            val_pred, val_seconds = predict(model, active_encoding, build["files"]["val"], features, val, seed=seed, split="val")
            test_pred, test_seconds = predict(model, active_encoding, build["files"]["test"], features, test, seed=seed, split="test")
            val_metrics = task.evaluate(val_pred, val)
            test_metrics = task.evaluate(test_pred, test)
            np.save(folder / "val_predictions.npy", val_pred)
            np.save(folder / "test_predictions.npy", test_pred)
            ap = []
            for true, predicted in zip(test.df.article_id, test_pred):
                relevant = np.isin(predicted, true)
                ap.append(float(((np.cumsum(relevant) / np.arange(1, 13)) * relevant).sum() / min(len(true), 12)))
            np.save(folder / "test_ap_per_user.npy", np.asarray(ap))
            metrics = {"model": kind, "seed": seed, "val_metrics": val_metrics, "test_metrics": test_metrics,
                       "inference_from_saved_model": True, "val_inference_seconds": val_seconds, "test_inference_seconds": test_seconds,
                       "config": config}
            (folder / "metrics.json").write_text(json.dumps(metrics, indent=2))
            record("manual_model_complete", f"Завершён {kind}; полный validation/test оценён из сохранённой модели", run_id,
                   status="complete", val_metrics=val_metrics, test_metrics=test_metrics, artifacts=str(folder.relative_to(ROOT)))
    record("manual_baseline_complete", "Дерево и LightGBM с ручными признаками завершены по выбранным seeds", RUN_ID, status="complete", artifacts=str(OUT.relative_to(ROOT)))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        record("manual_baseline_error", "Ошибка ручного baseline; требуется проверка лога", RUN_ID, status="failed", error=str(error))
        raise
