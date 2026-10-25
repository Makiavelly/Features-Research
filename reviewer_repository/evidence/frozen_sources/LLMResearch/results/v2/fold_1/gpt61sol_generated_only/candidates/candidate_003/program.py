import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    n = len(X)

    def scalar_map(series, key):
        return key.map(series).fillna(0)

    def pair_map(grouped, a, b):
        if len(grouped) == 0:
            return np.zeros(n)
        ix = pd.MultiIndex.from_arrays([a.to_numpy(), b.to_numpy()])
        return grouped.reindex(ix).fillna(0).to_numpy()

    if len(h):
        c_all = h.groupby("customer_id").size()
        i_all = h.groupby("article_id").size()
        c_rec = h.groupby("customer_id")["days_ago"].min()
        p_rec = h.groupby(["customer_id", "article_id"])["days_ago"].min()
        p_cnt = h.groupby(["customer_id", "article_id"]).size()

        out["f_customer_count_all"] = scalar_map(c_all, X["customer_id"])
        out["f_item_count_all"] = scalar_map(i_all, X["article_id"])
        out["f_customer_recency"] = scalar_map(c_rec, X["customer_id"])
        out["f_pair_recency"] = pair_map(p_rec, X["customer_id"], X["article_id"])
        out["f_pair_count"] = pair_map(p_cnt, X["customer_id"], X["article_id"])

        for d in (7, 30):
            z = h.loc[h["days_ago"] <= d]
            out["f_customer_count_" + str(d)] = scalar_map(
                z.groupby("customer_id").size(), X["customer_id"])
            out["f_item_count_" + str(d)] = scalar_map(
                z.groupby("article_id").size(), X["article_id"])

        for j, col in enumerate(("product_type_no", "section_no", "garment_group_no")):
            raw = X[("raw_i_" + col)].to_numpy()
            keys = pd.MultiIndex.from_arrays([X["customer_id"].to_numpy(), raw])
            g = h.groupby(["customer_id", col]).size()
            out["f_customer_" + str(j) + "_affinity"] = g.reindex(keys).fillna(0).to_numpy()

            z = h.loc[h["days_ago"] <= 30]
            g30 = z.groupby(["customer_id", col]).size()
            out["f_customer_" + str(j) + "_affinity30"] = (
                g30.reindex(keys).fillna(0).to_numpy()
            )

            gi = h.groupby(col).size()
            out["f_item_" + str(j) + "_popularity"] = (
                X[("raw_i_" + col)].map(gi).fillna(0).to_numpy()
            )
    else:
        for c in (
            "f_customer_count_all", "f_item_count_all", "f_customer_recency",
            "f_pair_recency", "f_pair_count", "f_customer_count_7",
            "f_item_count_7", "f_customer_count_30", "f_item_count_30",
            "f_customer_0_affinity", "f_customer_0_affinity30",
            "f_item_0_popularity", "f_customer_1_affinity",
            "f_customer_1_affinity30", "f_item_1_popularity",
            "f_customer_2_affinity", "f_customer_2_affinity30",
            "f_item_2_popularity"
        ):
            out[c] = 0.0

    for src in (
        "raw_u_age", "raw_u_active", "raw_u_club_member_status",
        "raw_i_product_code", "raw_i_product_type_no",
        "raw_i_section_no", "raw_i_garment_group_no"
    ):
        out["f_" + src[4:]] = X[src].to_numpy()

    out["f_customer_item_rate"] = (
        out["f_pair_count"] / (out["f_customer_count_all"] + 1.0)
    )
    out["f_item_share_recent"] = (
        out["f_item_count_7"] / (out["f_item_count_30"] + 1.0)
    )
    return out
