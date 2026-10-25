"""Behavioral tests for temporal leakage, program isolation and exact top-k."""
import tempfile
from pathlib import Path
import unittest

import numpy as np
import pandas as pd

from features import FeatureEngine, ITEM_COLUMNS, USER_COLUMNS, validate_program
from evaluate import topk


class ProtocolTests(unittest.TestCase):
    def test_forbidden_programs(self):
        for sql in ["(SELECT label FROM labels)", "read_parquet(1)", "sum(price); DROP TABLE tx", "customer_id", "rid", "avg(t_dat)"]:
            with self.subTest(sql=sql), self.assertRaises(ValueError):
                validate_program({"aggregates": [{"name": "f_bad", "keys": ["customer_id"], "sql": sql}], "derived": []})

    def test_catalog_topk_and_ties(self):
        ids = np.arange(105542, dtype=np.int64)
        rng = np.random.default_rng(42)
        scores = rng.integers(0, 100, len(ids)).astype(float)
        scores[-1] = 1000  # winner outside any small candidate prefix
        expected = ids[np.lexsort((ids, -scores))[:12]]
        np.testing.assert_array_equal(topk(scores, ids), expected)
        np.testing.assert_array_equal(topk(np.ones(len(ids)), ids), np.arange(12))

    def test_id_cardinality_and_global_category_allowed(self):
        program = {"aggregates": [
            {"name": "f_buyers", "keys": ["product_code"], "sql": "approx_count_distinct(customer_id)"},
            {"name": "f_items", "keys": ["customer_id"], "sql": "count(DISTINCT article_id)"}], "derived": []}
        self.assertEqual(validate_program(program), program)
        with self.assertRaises(ValueError):
            validate_program({"aggregates": [{"name": "f_bad", "keys": ["customer_id"], "sql": "sum(article_id)"}], "derived": []})

    def test_cutoff_future_and_label_isolation(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            items = pd.DataFrame({"article_id": [0, 1], **{name: [1, 2] for name in ITEM_COLUMNS}})
            users = pd.DataFrame({"customer_id": [0, 1], **{name: [1., 2.] for name in USER_COLUMNS}})
            users["club_member_status"] = ["A", "B"]
            users["fashion_news_frequency"] = ["A", "B"]
            items.to_parquet(folder / "article.parquet", index=False)
            users.to_parquet(folder / "customer.parquet", index=False)
            tx = pd.DataFrame({"customer_id": [0, 0, 0], "article_id": [0, 1, 0],
                               "t_dat": pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-03"]),
                               "price": [1., 3., 999999.], "sales_channel_id": [1, 2, 1]})
            tx.to_parquet(folder / "transactions.parquet", index=False)
            program = {"aggregates": [
                {"name": "f_volume", "keys": ["customer_id"], "sql": "count(*)"},
                {"name": "f_price", "keys": ["article_id"], "sql": "avg(price)"},
                {"name": "f_buyers", "keys": ["product_code"], "sql": "count(DISTINCT customer_id)"},
                {"name": "f_affinity", "keys": ["customer_id", "product_type_no"], "sql": "count(*) FILTER (WHERE days_ago <= 7)"}],
                "derived": [{"name": "f_ratio", "sql": "f_price / nullif(raw_u_age,0)"}]}
            pairs = pd.DataFrame({"customer_id": [0, 0, 1], "article_id": [1, 0, 1], "label": [0, 1, 1]})
            engine = FeatureEngine(folder / "scratch", folder)
            engine.prepare("2020-01-02", pairs.customer_id.values, program)
            frame = engine.frame(pairs)
            self.assertEqual(frame.f_volume.iloc[0], 2)  # cutoff row included
            self.assertEqual(frame.f_price.iloc[1], 1)   # future 999999 excluded
            self.assertEqual(frame.f_affinity.iloc[0], 1)
            self.assertEqual(frame.f_buyers.iloc[0], 1)
            first = engine.matrix(pairs)
            pairs.label = 1-pairs.label
            np.testing.assert_array_equal(first, engine.matrix(pairs))
            self.assertFalse(any(name in frame for name in ["label", "customer_id", "article_id", "timestamp"]))
            engine.close()
            # Mutating a future transaction cannot change any feature.
            tx.loc[2, "price"] = -999999.
            tx.to_parquet(folder / "transactions.parquet", index=False)
            engine = FeatureEngine(folder / "scratch", folder)
            engine.prepare("2020-01-02", pairs.customer_id.values, program)
            np.testing.assert_array_equal(first, engine.matrix(pairs))
            engine.close()


if __name__ == "__main__":
    unittest.main()
