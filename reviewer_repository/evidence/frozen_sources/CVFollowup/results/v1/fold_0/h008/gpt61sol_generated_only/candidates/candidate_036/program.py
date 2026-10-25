import pandas as pd
import numpy as np


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    c = X["customer_id"]
    a = X["article_id"]

    def mapped(keys, values, fill=None):
        result = keys.map(values)
        return result.fillna(fill) if fill is not None else result

    def pair_count(z):
        counts = z.groupby(["customer_id", "article_id"]).size()
        keys = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
        return pd.Series(counts.reindex(keys).to_numpy(), index=X.index).fillna(0)

    def category_count(z, raw_col, hist_col):
        sentinel = -999999
        cat = z[hist_col].fillna(sentinel)
        counts = z.assign(_cat=cat).groupby(["customer_id", "_cat"]).size()
        keys = pd.MultiIndex.from_arrays(
            [c.to_numpy(), X[raw_col].fillna(sentinel).to_numpy()]
        )
        return pd.Series(counts.reindex(keys).to_numpy(), index=X.index).fillna(0)

    if h.empty:
        for name in (
            "item_pop_7d", "item_pop_30d", "item_pop_90d", "item_pop_all",
            "item_unique_buyers", "item_recency", "item_trend",
            "user_item_30d", "user_item_all", "user_item_recency",
            "user_recency", "user_purchases_7d", "user_purchases_30d",
            "user_purchases_90d", "user_purchases_all", "user_type_30d",
            "user_type_all", "user_product_30d", "user_department_30d",
            "user_section_30d", "user_garment_90d", "item_mean_price",
            "user_price_mean", "user_channel1_share", "age",
        ):
            out["f_" + name] = np.nan
        return out

    h7 = h.loc[h["days_ago"] <= 7]
    h30 = h.loc[h["days_ago"] <= 30]
    h90 = h.loc[h["days_ago"] <= 90]

    for label, z in (("7d", h7), ("30d", h30), ("90d", h90), ("all", h)):
        out["f_item_pop_" + label] = mapped(a, z.groupby("article_id").size(), 0)

    out["f_item_unique_buyers"] = mapped(
        a, h.groupby("article_id")["customer_id"].nunique(), 0
    )
    out["f_item_recency"] = mapped(
        a, h.groupby("article_id")["days_ago"].min()
    )
    pop7 = a.map(h7.groupby("article_id").size()).fillna(0)
    pop90 = a.map(h90.groupby("article_id").size()).fillna(0)
    out["f_item_trend"] = np.log1p(pop7) - np.log1p(pop90 / 13.0)

    out["f_user_item_30d"] = pair_count(h30)
    out["f_user_item_all"] = pair_count(h)
    pair_recent = h.groupby(["customer_id", "article_id"])["days_ago"].min()
    keys = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])
    out["f_user_item_recency"] = pd.Series(
        pair_recent.reindex(keys).to_numpy(), index=X.index
    )

    out["f_user_recency"] = mapped(c, h.groupby("customer_id")["days_ago"].min())
    for label, z in (("7d", h7), ("30d", h30), ("90d", h90), ("all", h)):
        out["f_user_purchases_" + label] = mapped(
            c, z.groupby("customer_id").size(), 0
        )

    out["f_user_type_30d"] = category_count(
        h30, "raw_i_product_type_no", "product_type_no"
    )
    out["f_user_type_all"] = category_count(
        h, "raw_i_product_type_no", "product_type_no"
    )
    out["f_user_product_30d"] = category_count(
        h30, "raw_i_product_code", "product_code"
    )
    out["f_user_department_30d"] = category_count(
        h30, "raw_i_department_no", "department_no"
    )
    out["f_user_section_30d"] = category_count(
        h30, "raw_i_section_no", "section_no"
    )
    out["f_user_garment_90d"] = category_count(
        h90, "raw_i_garment_group_no", "garment_group_no"
    )

    out["f_item_mean_price"] = mapped(a, h.groupby("article_id")["price"].mean())
    out["f_user_price_mean"] = mapped(c, h.groupby("customer_id")["price"].mean())
    channel_share = h.assign(_ch=(h["sales_channel_id"] == 1).astype(float))
    out["f_user_channel1_share"] = mapped(
        c, channel_share.groupby("customer_id")["_ch"].mean()
    )
    out["f_age"] = X["raw_u_age"]

    return out.replace([np.inf, -np.inf], np.nan)
