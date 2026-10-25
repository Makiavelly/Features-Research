import pandas as pd
import numpy as np


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    c = X["customer_id"]
    a = X["article_id"]

    def map_values(keys, values, default=0.0):
        return keys.map(values).fillna(default).to_numpy()

    def map_pairs(values, default=0.0):
        pairs = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return values.reindex(pairs).fillna(default).to_numpy()

    h = history
    names = (
        "f_item_count_14d", "f_item_count_60d", "f_item_count_all",
        "f_item_recency", "f_item_mean_price", "f_user_count_14d",
        "f_user_count_all", "f_pair_count_14d", "f_pair_count_all",
        "f_pair_recency", "f_user_department_count", "f_user_type_count",
    )
    for name in names:
        out[name] = np.nan if "recency" in name else 0.0

    if not h.empty:
        d = h["days_ago"]
        for window in (14, 60):
            q = h.loc[d <= window]
            out[f"f_item_count_{window}d"] = map_values(
                a, q.groupby("article_id").size()
            )
        ig = h.groupby("article_id")
        ug = h.groupby("customer_id")
        pg = h.groupby(["customer_id", "article_id"])

        out["f_item_count_all"] = map_values(a, ig.size())
        out["f_item_recency"] = map_values(a, ig["days_ago"].min(), np.nan)
        out["f_item_mean_price"] = map_values(a, ig["price"].mean(), np.nan)
        q = h.loc[d <= 14]
        out["f_user_count_14d"] = map_values(c, q.groupby("customer_id").size())
        out["f_user_count_all"] = map_values(c, ug.size())
        out["f_pair_count_14d"] = map_pairs(
            q.groupby(["customer_id", "article_id"]).size()
        )
        out["f_pair_count_all"] = map_pairs(pg.size())
        out["f_pair_recency"] = map_pairs(pg["days_ago"].min(), np.nan)

        for hc, xc, name in (
            ("department_no", "raw_i_department_no", "f_user_department_count"),
            ("product_type_no", "raw_i_product_type_no", "f_user_type_count"),
        ):
            counts = h.groupby(["customer_id", hc]).size()
            keys = pd.MultiIndex.from_arrays(
                [c.to_numpy(), X[xc].to_numpy()]
            )
            out[name] = counts.reindex(keys).fillna(0).to_numpy()

    return out.reindex(X.index)
