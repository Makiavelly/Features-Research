import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def single_map(group_col, value_col=None, window=None, agg="size"):
        h = history
        if window is not None:
            h = h.loc[h["days_ago"] <= window]
        if value_col is None:
            s = h.groupby(group_col).size()
        elif agg == "min":
            s = h.groupby(group_col)[value_col].min()
        else:
            s = h.groupby(group_col)[value_col].size()
        return X[group_col].map(s).fillna(0).to_numpy()

    def pair_map(hcols, xcols, window=None, agg="size", value_col=None):
        h = history
        if window is not None:
            h = h.loc[h["days_ago"] <= window]
        keys = h.groupby(hcols)
        if agg == "min":
            s = keys[value_col].min()
        else:
            s = keys.size()
        idx = pd.MultiIndex.from_arrays(
            [X[c].to_numpy() for c in xcols], names=hcols
        )
        return s.reindex(idx).fillna(0).to_numpy()

    out["f_item_count_7d"] = single_map("article_id", window=7)
    out["f_item_count_30d"] = single_map("article_id", window=30)
    out["f_item_count_all"] = single_map("article_id")
    out["f_item_recency"] = single_map("article_id", "days_ago", agg="min")

    out["f_user_count_7d"] = single_map("customer_id", window=7)
    out["f_user_count_30d"] = single_map("customer_id", window=30)
    out["f_user_count_all"] = single_map("customer_id")
    out["f_user_recency"] = single_map("customer_id", "days_ago", agg="min")

    out["f_pair_count_30d"] = pair_map(
        ["customer_id", "article_id"], ["customer_id", "article_id"], 30
    )
    out["f_pair_count_all"] = pair_map(
        ["customer_id", "article_id"], ["customer_id", "article_id"]
    )
    out["f_pair_recency"] = pair_map(
        ["customer_id", "article_id"], ["customer_id", "article_id"],
        agg="min", value_col="days_ago"
    )

    cats = [
        ("product_code", "raw_i_product_code"),
        ("product_type_no", "raw_i_product_type_no"),
        ("department_no", "raw_i_department_no"),
        ("section_no", "raw_i_section_no"),
        ("garment_group_no", "raw_i_garment_group_no"),
    ]
    for j, (hc, xc) in enumerate(cats):
        out["f_affinity_%d_30d" % j] = pair_map(
            ["customer_id", hc], ["customer_id", xc], 30
        )
        out["f_affinity_%d_all" % j] = pair_map(
            ["customer_id", hc], ["customer_id", xc]
        )

    for j, (hc, xc) in enumerate(cats[:4]):
        out["f_item_cat_%d_30d" % j] = pair_map(
            ["article_id", hc], ["article_id", xc], 30
        )

    out["f_user_age"] = X["raw_u_age"].to_numpy()
    out["f_user_active"] = X["raw_u_active"].to_numpy()
    out["f_user_club"] = X["raw_u_club_member_status"].to_numpy()
    out["f_item_product_code"] = X["raw_i_product_code"].to_numpy()
    out["f_item_product_type"] = X["raw_i_product_type_no"].to_numpy()
    out["f_item_department"] = X["raw_i_department_no"].to_numpy()
    out["f_item_section"] = X["raw_i_section_no"].to_numpy()
    out["f_item_garment"] = X["raw_i_garment_group_no"].to_numpy()

    out["f_item_rate_7_30"] = out["f_item_count_7d"] / (out["f_item_count_30d"] + 1.0)
    out["f_user_rate_7_30"] = out["f_user_count_7d"] / (out["f_user_count_30d"] + 1.0)
    out["f_pair_share"] = out["f_pair_count_all"] / (out["f_user_count_all"] + 1.0)
    out["f_recency_score"] = np.exp(-out["f_item_recency"] / 30.0)
    return out.replace([np.inf, -np.inf], np.nan)
