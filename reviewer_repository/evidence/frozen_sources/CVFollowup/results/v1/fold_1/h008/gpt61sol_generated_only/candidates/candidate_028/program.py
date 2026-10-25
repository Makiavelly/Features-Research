import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_count_all", "f_item_users_30d", "f_item_trend_7_30",
        "f_user_count_7d", "f_user_count_30d", "f_user_count_all",
        "f_user_recency", "f_pair_count_all", "f_pair_count_30d",
        "f_pair_recency", "f_user_product_count", "f_user_type_count",
        "f_user_department_count", "f_user_section_count",
        "f_item_mean_price", "f_item_channel2_share",
        "f_user_age", "f_user_club", "f_user_news"
    ]
    out = pd.DataFrame(index=X.index)

    if history is None or len(history) == 0:
        for name in names:
            out[name] = np.nan if name in ("f_user_recency", "f_pair_recency",
                                           "f_item_mean_price") else 0.0
        return out[names]

    h = history
    d = pd.to_numeric(h["days_ago"], errors="coerce")
    h7 = h.loc[d <= 7]
    h30 = h.loc[d <= 30]
    h90 = h.loc[d <= 90]

    c7 = h7.groupby("article_id").size()
    c30 = h30.groupby("article_id").size()
    c90 = h90.groupby("article_id").size()
    call = h.groupby("article_id").size()

    out["f_item_count_7d"] = X["article_id"].map(c7).fillna(0).to_numpy()
    out["f_item_count_30d"] = X["article_id"].map(c30).fillna(0).to_numpy()
    out["f_item_count_90d"] = X["article_id"].map(c90).fillna(0).to_numpy()
    out["f_item_count_all"] = X["article_id"].map(call).fillna(0).to_numpy()

    iu30 = h30.groupby("article_id")["customer_id"].nunique()
    out["f_item_users_30d"] = X["article_id"].map(iu30).fillna(0).to_numpy()
    a7 = X["article_id"].map(c7).fillna(0).to_numpy(dtype=float)
    a30 = X["article_id"].map(c30).fillna(0).to_numpy(dtype=float)
    out["f_item_trend_7_30"] = a7 / (a30 + 1.0)

    u7 = h7.groupby("customer_id").size()
    u30 = h30.groupby("customer_id").size()
    uall = h.groupby("customer_id").size()
    urec = h.groupby("customer_id")["days_ago"].min()
    out["f_user_count_7d"] = X["customer_id"].map(u7).fillna(0).to_numpy()
    out["f_user_count_30d"] = X["customer_id"].map(u30).fillna(0).to_numpy()
    out["f_user_count_all"] = X["customer_id"].map(uall).fillna(0).to_numpy()
    out["f_user_recency"] = X["customer_id"].map(urec).to_numpy()

    pair_all = h.groupby(["customer_id", "article_id"]).agg(
        count=("days_ago", "size"),
        recency=("days_ago", "min")
    )
    pair30 = h30.groupby(["customer_id", "article_id"]).size()
    keys = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(),
        X["article_id"].to_numpy()
    ])
    out["f_pair_count_all"] = pair_all["count"].reindex(keys).fillna(0).to_numpy()
    out["f_pair_count_30d"] = pair30.reindex(keys).fillna(0).to_numpy()
    out["f_pair_recency"] = pair_all["recency"].reindex(keys).to_numpy()

    for hist_col, raw_col, name in (
        ("product_code", "raw_i_product_code", "f_user_product_count"),
        ("product_type_no", "raw_i_product_type_no", "f_user_type_count"),
        ("department_no", "raw_i_department_no", "f_user_department_count"),
        ("section_no", "raw_i_section_no", "f_user_section_count"),
    ):
        agg = h30.groupby(["customer_id", hist_col]).size()
        catkeys = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X[raw_col].to_numpy()
        ])
        out[name] = agg.reindex(catkeys).fillna(0).to_numpy()

    price = h.groupby("article_id")["price"].mean()
    out["f_item_mean_price"] = X["article_id"].map(price).to_numpy()

    channel = h.groupby("article_id")["sales_channel_id"].agg(
        total="size",
        channel2=lambda s: (s == 2).sum()
    )
    chshare = channel["channel2"] / channel["total"]
    out["f_item_channel2_share"] = X["article_id"].map(chshare).fillna(0).to_numpy()

    out["f_user_age"] = pd.to_numeric(X["raw_u_age"], errors="coerce").to_numpy()
    out["f_user_club"] = pd.to_numeric(
        X["raw_u_club_member_status"], errors="coerce"
    ).to_numpy()
    out["f_user_news"] = pd.to_numeric(
        X["raw_u_fashion_news_frequency"], errors="coerce"
    ).to_numpy()

    return out[names]
