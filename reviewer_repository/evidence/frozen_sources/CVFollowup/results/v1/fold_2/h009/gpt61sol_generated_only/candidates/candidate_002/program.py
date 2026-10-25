import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    h = history
    if len(h) == 0:
        for name in (
            "f_pair_7d", "f_pair_30d", "f_pair_180d", "f_pair_recency",
            "f_user_7d", "f_user_30d", "f_user_180d", "f_item_7d",
            "f_item_30d", "f_item_180d", "f_user_department", "f_user_section"
        ):
            out[name] = np.zeros(n, dtype=float)
        return out

    def grouped_count(frame, keys):
        return frame.groupby(keys, sort=False).size()

    def pair_values(frame, keys, target_keys):
        s = grouped_count(frame, keys)
        idx = pd.MultiIndex.from_arrays(
            [X[k].to_numpy() for k in target_keys],
            names=keys
        )
        return s.reindex(idx).to_numpy(dtype=float)

    def user_category_values(category_col, raw_col):
        s = grouped_count(h, ["customer_id", category_col])
        idx = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[raw_col].to_numpy()],
            names=["customer_id", category_col]
        )
        return s.reindex(idx).to_numpy(dtype=float)

    r7 = h.loc[h["days_ago"] <= 7]
    r30 = h.loc[h["days_ago"] <= 30]
    r180 = h.loc[h["days_ago"] <= 180]

    out["f_pair_7d"] = pair_values(
        r7, ["customer_id", "article_id"], ["customer_id", "article_id"]
    )
    out["f_pair_30d"] = pair_values(
        r30, ["customer_id", "article_id"], ["customer_id", "article_id"]
    )
    out["f_pair_180d"] = pair_values(
        r180, ["customer_id", "article_id"], ["customer_id", "article_id"]
    )

    pair_recency = h.groupby(
        ["customer_id", "article_id"], sort=False
    )["days_ago"].min()
    pair_idx = pd.MultiIndex.from_arrays(
        [X["customer_id"].to_numpy(), X["article_id"].to_numpy()],
        names=["customer_id", "article_id"]
    )
    out["f_pair_recency"] = pair_recency.reindex(pair_idx).to_numpy(dtype=float)

    for suffix, frame in (("7d", r7), ("30d", r30), ("180d", r180)):
        users = frame.groupby("customer_id", sort=False).size()
        items = frame.groupby("article_id", sort=False).size()
        out["f_user_" + suffix] = X["customer_id"].map(users).to_numpy(dtype=float)
        out["f_item_" + suffix] = X["article_id"].map(items).to_numpy(dtype=float)

    out["f_user_department"] = user_category_values(
        "department_no", "raw_i_department_no"
    )
    out["f_user_section"] = user_category_values(
        "section_no", "raw_i_section_no"
    )

    for c in out.columns:
        out[c] = pd.to_numeric(out[c], errors="coerce").replace(
            [np.inf, -np.inf], np.nan
        )
    return out.reindex(index=X.index)
