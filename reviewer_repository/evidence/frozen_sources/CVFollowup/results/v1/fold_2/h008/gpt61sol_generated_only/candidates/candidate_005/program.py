import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    if h.empty:
        for name in (
            "f_pair_30d", "f_pair_90d", "f_pair_all", "f_pair_recency",
            "f_customer_30d", "f_customer_all", "f_item_30d", "f_item_all",
            "f_item_recency", "f_customer_product_90d", "f_customer_type_90d",
            "f_customer_section_90d", "f_item_channel_90d", "f_user_age"
        ):
            out[name] = 0.0
        return out

    pair_h = h.groupby(["customer_id", "article_id"], sort=False)
    for days, name in ((30, "f_pair_30d"), (90, "f_pair_90d")):
        counts = h.loc[h["days_ago"] <= days].groupby(
            ["customer_id", "article_id"], sort=False
        ).size()
        out[name] = pd.MultiIndex.from_frame(
            X[["customer_id", "article_id"]]
        ).map(counts).to_numpy(dtype=float)
    counts = pair_h.size()
    out["f_pair_all"] = pd.MultiIndex.from_frame(
        X[["customer_id", "article_id"]]
    ).map(counts).to_numpy(dtype=float)
    rec = pair_h["days_ago"].min()
    out["f_pair_recency"] = pd.MultiIndex.from_frame(
        X[["customer_id", "article_id"]]
    ).map(rec).to_numpy(dtype=float)

    for days, name in ((30, "f_customer_30d"), (0, "f_customer_all")):
        hh = h if days == 0 else h.loc[h["days_ago"] <= days]
        counts = hh.groupby("customer_id", sort=False).size()
        out[name] = X["customer_id"].map(counts).fillna(0).to_numpy(dtype=float)

    for days, name in ((30, "f_item_30d"), (0, "f_item_all")):
        hh = h if days == 0 else h.loc[h["days_ago"] <= days]
        counts = hh.groupby("article_id", sort=False).size()
        out[name] = X["article_id"].map(counts).fillna(0).to_numpy(dtype=float)
    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    ).to_numpy(dtype=float)

    recent = h.loc[h["days_ago"] <= 90]
    for raw, hc, name in (
        ("raw_i_product_code", "product_code", "f_customer_product_90d"),
        ("raw_i_product_type_no", "product_type_no", "f_customer_type_90d"),
        ("raw_i_section_no", "section_no", "f_customer_section_90d"),
    ):
        counts = recent.groupby(["customer_id", hc], sort=False).size()
        keys = pd.MultiIndex.from_arrays([X["customer_id"], X[raw]])
        out[name] = keys.map(counts).to_numpy(dtype=float)

    channel = recent.groupby(["article_id", "sales_channel_id"], sort=False).size()
    # Popularity of the article in its more-used channel, normalized by article demand.
    ch1 = h.loc[(h["days_ago"] <= 90) & (h["sales_channel_id"] == 1)].groupby(
        "article_id", sort=False
    ).size()
    ch2 = h.loc[(h["days_ago"] <= 90) & (h["sales_channel_id"] == 2)].groupby(
        "article_id", sort=False
    ).size()
    denom = ch1.add(ch2, fill_value=0)
    out["f_item_channel_90d"] = X["article_id"].map(
        (ch1 - ch2) / denom.replace(0, np.nan)
    ).to_numpy(dtype=float)
    out["f_user_age"] = pd.to_numeric(X["raw_u_age"], errors="coerce").to_numpy()
    return out.replace([np.inf, -np.inf], np.nan).astype(float)
