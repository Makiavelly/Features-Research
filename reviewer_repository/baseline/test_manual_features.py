"""Verify date boundaries and that adding future transactions cannot change features."""
from pathlib import Path
import tempfile

import pandas as pd
import numpy as np
import joblib
import lightgbm as lgb
from pandas.testing import assert_frame_equal

from manual_features import ARTICLE_CODES, ManualFeatures, ROOT
from run_manual_tree import TreeEncoding, dense, predict
from sklearn.tree import DecisionTreeClassifier


def main():
    with tempfile.TemporaryDirectory(dir=ROOT / "baseline") as temporary:
        folder = Path(temporary)
        articles = pd.DataFrame({"article_id": [0, 1, 2], **{c: [10, 20, 30] for c in ARTICLE_CODES}})
        customers = pd.DataFrame({"customer_id": [0, 1], "age": [25., 40.], "FN": [1., None], "Active": [1., None],
                                  "club_member_status": ["ACTIVE", "ACTIVE"], "fashion_news_frequency": ["Regularly", "NONE"]})
        tx = pd.DataFrame({"t_dat": pd.to_datetime(["2020-09-01", "2020-09-05", "2020-09-07", "2020-09-08"]),
                           "customer_id": [0, 0, 0, 0], "article_id": [0, 0, 1, 2],
                           "price": [.1, .2, .3, 999.], "sales_channel_id": [1, 2, 1, 2]})
        articles.to_parquet(folder / "article.parquet", index=False)
        customers.to_parquet(folder / "customer.parquet", index=False)
        tx.iloc[:3].to_parquet(folder / "transactions.parquet", index=False)
        pairs = pd.DataFrame({"customer_id": [0, 0, 1], "article_id": [0, 2, 1], "label": [1, 0, 0]})
        engine = ManualFeatures(folder, folder / "cache", memory_limit="128MB")
        engine.prepare("2020-09-07", [0, 1])
        original = engine.frame(pairs).sort_values(["customer_id", "article_id"]).reset_index(drop=True)
        row = original[(original.customer_id == 0) & (original.article_id == 0)].iloc[0]
        assert row.u_count_all == 3 and row.p_count_all == 2
        assert row.p_recency_days == 2 and row.u_count_week1 == 3
        assert not {"customer_id", "article_id", "timestamp", "label"}.intersection(engine.feature_names)
        engine.write(pairs, folder / "features.parquet")
        saved = pd.read_parquet(folder / "features.parquet")
        assert len(saved) == len(pairs) and len(engine.feature_names) > 100
        feature_names = engine.feature_names
        categorical_names = engine.categorical_names
        values = dense(saved, feature_names)
        encoding = TreeEncoding(feature_names, categorical_names).fit(values)
        model = DecisionTreeClassifier(max_depth=2, min_samples_leaf=1, random_state=42).fit(encoding.transform(values), saved.label.values)
        bundle = {"model": model, "encoder": encoding.encoder}
        joblib.dump(bundle, folder / "tree.joblib")
        loaded = joblib.load(folder / "tree.joblib")
        assert np.array_equal(model.predict_proba(encoding.transform(values)), loaded["model"].predict_proba(encoding.transform(values)))
        candidates = pd.DataFrame({"customer_id": [0, 1], "candidates": [[0, 1, 2], [0, 1, 2]]})
        candidates.to_parquet(folder / "candidates.parquet", index=False)
        eval_pairs = candidates.explode("candidates").rename(columns={"candidates": "article_id"})
        eval_pairs.article_id = eval_pairs.article_id.astype(np.int64)
        engine.write(eval_pairs, folder / "eval.parquet")
        target = type("Target", (), {"df": pd.DataFrame({"customer_id": [0, 1]}), "__len__": lambda self: len(self.df)})()
        tree_pred, _ = predict(loaded["model"], encoding, [folder / "eval.parquet"], feature_names, target, k=2, candidate_file=folder / "candidates.parquet")
        assert tree_pred.shape == (2, 2) and tree_pred[0, 0] == 0
        booster = lgb.train({"objective": "binary", "verbosity": -1, "min_data_in_leaf": 1, "num_leaves": 3, "num_threads": 1},
                            lgb.Dataset(values, label=saved.label.values), num_boost_round=5)
        booster.save_model(str(folder / "lgb.txt"))
        reloaded = lgb.Booster(model_file=str(folder / "lgb.txt"))
        assert np.allclose(booster.predict(values), reloaded.predict(values))
        lgb_pred, _ = predict(reloaded, None, [folder / "eval.parquet"], feature_names, target, k=2, candidate_file=folder / "candidates.parquet")
        assert lgb_pred.shape == (2, 2)
        engine.close()
        tx.to_parquet(folder / "transactions.parquet", index=False)
        engine = ManualFeatures(folder, folder / "cache2", memory_limit="128MB")
        engine.prepare("2020-09-07", [0, 1])
        changed = engine.frame(pairs).sort_values(["customer_id", "article_id"]).reset_index(drop=True)
        assert_frame_equal(original, changed)
        candidates = engine.history_candidates()
        assert 2 not in candidates.iloc[0].candidates
        engine.close()
    print("PASS: date safety, 126 manual features, train/reload DecisionTree and LightGBM, streaming top-k and no labels/IDs in model inputs")


if __name__ == "__main__":
    main()
