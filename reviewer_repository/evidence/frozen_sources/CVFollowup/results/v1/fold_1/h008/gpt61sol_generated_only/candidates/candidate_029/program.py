import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    static_cols = (
        "raw_u_age", "raw_u_fn", "raw_u_active",
        "raw_u_club_member_status", "raw_u_fashion_news_frequency",
        "raw_i_product_type_no", "raw_i_colour_group_code",
        "raw_i_department_no", "raw_i_section_no",
        "raw_i_garment_group_no", "raw_i_index_group_no"
    )
    for col in static_cols:
        out["f_" + col[4:]] = X[col].to_numpy(dtype=float)

    def one_map(series, key, fill=0.0):
        if series.empty:
            return np.full(n, fill, dtype=float)
        return X[key].map(series).fillna(fill).to_numpy(dtype=float)

    def pair_map(series, raw_col, fill=0.0):
        if series.empty:
            return np.full(n, fill, dtype=float)
        idx = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[raw_col].to_numpy()]
        )
        vals = series.reindex(idx).to_numpy(dtype=float)
        return np.nan_to_num(vals, nan=fill, posinf=fill, neginf=fill)

    if h.empty:
        names = (
            "f_user_item_count", "f_user_item_count_30d",
            "f_user_item_recency", "f_item_pop_all",
            "f_item_pop_7d", "f_item_pop_30d", "f_item_recency",
            "f_user_activity_7d", "f_user_activity_30d",
            "f_user_activity_90d", "f_user_recency",
            "f_user_department_90d", "f_user_product_type_90d",
            "f_user_garment_90d", "f_user_department_recency",
            "f_item_trend_7_30", "f_item_price_mean",
            "f_user_price_mean", "f_user_item_price_mean",
            "f_user_item_vs_popularity"
        )
        for name in names:
            out[name] = 0.0
        return out

    h7 = h.loc[h["days_ago"] <= 7]
    h30 = h.loc[h["days_ago"] <= 30]
    h90 = h.loc[h["days_ago"] <= 90]

    ui = h.groupby(["customer_id", "article_id"], sort=False)
    item = h.groupby("article_id", sort=False)
    user = h.groupby("customer_id", sort=False)

    out["f_user_item_count"] = pair_map(ui.size(), "article_id")
    out["f_user_item_count_30d"] = pair_map(
        h30.groupby(["customer_id", "article_id"], sort=False).size(),
        "article_id"
    )
    out["f_user_item_recency"] = pair_map(
        ui["days_ago"].min(), "article_id", 9999.0
    )

    item_all = item.size()
    item_7 = h7.groupby("article_id", sort=False).size()
    item_30 = h30.groupby("article_id", sort=False).size()

    out["f_item_pop_all"] = one_map(item_all, "article_id")
    out["f_item_pop_7d"] = one_map(item_7, "article_id")
    out["f_item_pop_30d"] = one_map(item_30, "article_id")
    out["f_item_recency"] = one_map(item["days_ago"].min(), "article_id", 9999.0)

    p7 = out["f_item_pop_7d"].to_numpy(dtype=float)
    p30 = out["f_item_pop_30d"].to_numpy(dtype=float)
    out["f_item_trend_7_30"] = p7 / np.maximum(p30, 1.0)

    out["f_user_activity_7d"] = one_map(
        h7.groupby("customer_id", sort=False).size(), "customer_id"
    )
    out["f_user_activity_30d"] = one_map(
        h30.groupby("customer_id", sort=False).size(), "customer_id"
    )
    out["f_user_activity_90d"] = one_map(
        h90.groupby("customer_id", sort=False).size(), "customer_id"
    )
    out["f_user_recency"] = one_map(
        user["days_ago"].min(), "customer_id", 9999.0
    )

    for hist_col, raw_col, name in (
        ("department_no", "raw_i_department_no", "f_user_department_90d"),
        ("product_type_no", "raw_i_product_type_no", "f_user_product_type_90d"),
        ("garment_group_no", "raw_i_garment_group_no", "f_user_garment_90d"),
    ):
        counts = h90.groupby(["customer_id", hist_col], sort=False).size()
        out[name] = pair_map(counts, raw_col)

    dept_rec = h.groupby(
        ["customer_id", "department_no"], sort=False
    )["days_ago"].min()
    out["f_user_department_recency"] = pair_map(
        dept_rec, "raw_i_department_no", 9999.0
    )

    item_price = item["price"].mean()
    user_price = user["price"].mean()
    ui_price = ui["price"].mean()

    out["f_item_price_mean"] = one_map(item_price, "article_id")
    out["f_user_price_mean"] = one_map(user_price, "customer_id")
    out["f_user_item_price_mean"] = pair_map(ui_price, "article_id")

    ui_count = out["f_user_item_count"].to_numpy(dtype=float)
    item_count = out["f_item_pop_all"].to_numpy(dtype=float)
    out["f_user_item_vs_popularity"] = ui_count / np.maximum(item_count, 1.0)

    return out.replace([np.inf, -np.inf], np.nan)
