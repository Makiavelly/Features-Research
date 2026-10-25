import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    c = X["customer_id"]
    a = X["article_id"]

    names = (
        "f_item_purchases_7d", "f_item_purchases_30d",
        "f_item_purchases_all", "f_item_recency",
        "f_user_purchases_7d", "f_user_purchases_30d",
        "f_user_purchases_all", "f_user_recency",
        "f_pair_purchases_30d", "f_pair_purchases_all",
        "f_pair_recency", "f_user_department_purchases"
    )
    for name in names:
        out[name] = np.nan if name.endswith("recency") else 0.0

    if history.empty:
        return out

    def item_map(series):
        return a.map(series).fillna(0).to_numpy()

    def user_map(series):
        return c.map(series).fillna(0).to_numpy()

    pair_keys = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])

    def pair_map(series):
        return series.reindex(pair_keys).fillna(0).to_numpy()

    h = history
    days = h["days_ago"]

    for window in (7, 30):
        q = h.loc[days <= window]
        out[f"f_item_purchases_{window}d"] = item_map(q.groupby("article_id").size())
        out[f"f_user_purchases_{window}d"] = user_map(q.groupby("customer_id").size())

    item_groups = h.groupby("article_id")
    user_groups = h.groupby("customer_id")
    pair_groups = h.groupby(["customer_id", "article_id"])

    out["f_item_purchases_all"] = item_map(item_groups.size())
    out["f_item_recency"] = a.map(item_groups["days_ago"].min()).to_numpy()
    out["f_user_purchases_all"] = user_map(user_groups.size())
    out["f_user_recency"] = c.map(user_groups["days_ago"].min()).to_numpy()

    recent = h.loc[days <= 30]
    out["f_pair_purchases_30d"] = pair_map(
        recent.groupby(["customer_id", "article_id"]).size()
    )
    pair_counts = pair_groups.size()
    out["f_pair_purchases_all"] = pair_map(pair_counts)
    out["f_pair_recency"] = pair_map(pair_groups["days_ago"].min())

    category_counts = h.groupby(["customer_id", "department_no"]).size()
    category_keys = pd.MultiIndex.from_arrays(
        [c.to_numpy(), X["raw_i_department_no"].to_numpy()]
    )
    out["f_user_department_purchases"] = (
        category_counts.reindex(category_keys).fillna(0).to_numpy()
    )

    return out.reindex(X.index)
