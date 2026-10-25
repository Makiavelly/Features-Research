import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def mapped(s, key):
        return key.map(s).fillna(0).to_numpy()

    def pair_values(s):
        if len(s) == 0:
            return np.zeros(n)
        keys = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(),
            X["article_id"].to_numpy()
        ])
        return s.reindex(keys).fillna(0).to_numpy()

    if len(history):
        h = history
        ca = h.groupby("customer_id").size()
        ia = h.groupby("article_id").size()
        cr = h.groupby("customer_id")["days_ago"].min()
        pc = h.groupby(["customer_id", "article_id"]).size()
        pr = h.groupby(["customer_id", "article_id"])["days_ago"].min()

        out["f_customer_count"] = mapped(ca, X["customer_id"])
        out["f_item_count"] = mapped(ia, X["article_id"])
        out["f_customer_recency"] = mapped(cr, X["customer_id"])
        out["f_pair_count"] = pair_values(pc)
        out["f_pair_recency"] = pair_values(pr)

        for d in (7, 30, 90):
            z = h.loc[h["days_ago"] <= d]
            out["f_customer_count_" + str(d)] = mapped(
                z.groupby("customer_id").size(), X["customer_id"])
            out["f_item_count_" + str(d)] = mapped(
                z.groupby("article_id").size(), X["article_id"])
            out["f_pair_count_" + str(d)] = pair_values(
                z.groupby(["customer_id", "article_id"]).size())

        for j, col in enumerate(("product_type_no", "section_no",
                                 "garment_group_no", "department_no")):
            raw = X["raw_i_" + col].to_numpy()
            keys = pd.MultiIndex.from_arrays([
                X["customer_id"].to_numpy(), raw
            ])
            g = h.groupby(["customer_id", col]).size()
            out["f_affinity_" + str(j)] = g.reindex(keys).fillna(0).to_numpy()

            z = h.loc[h["days_ago"] <= 30]
            g = z.groupby(["customer_id", col]).size()
            out["f_affinity30_" + str(j)] = (
                g.reindex(keys).fillna(0).to_numpy()
            )

            g = h.groupby(col).size()
            out["f_category_pop_" + str(j)] = (
                X["raw_i_" + col].map(g).fillna(0).to_numpy()
            )

        avg_price = h.groupby("customer_id")["price"].mean()
        item_price = h.groupby("article_id")["price"].mean()
        out["f_customer_price"] = mapped(avg_price, X["customer_id"])
        out["f_item_price"] = mapped(item_price, X["article_id"])
    else:
        names = [
            "f_customer_count", "f_item_count", "f_customer_recency",
            "f_pair_count", "f_pair_recency"
        ]
        for d in (7, 30, 90):
            names += ["f_customer_count_" + str(d),
                      "f_item_count_" + str(d), "f_pair_count_" + str(d)]
        for j in range(4):
            names += ["f_affinity_" + str(j), "f_affinity30_" + str(j),
                      "f_category_pop_" + str(j)]
        names += ["f_customer_price", "f_item_price"]
        for name in names:
            out[name] = 0.0

    out["f_pair_rate"] = (
        out["f_pair_count"] / (out["f_customer_count"] + 1.0)
    )
    out["f_pair_recent_rate"] = (
        out["f_pair_count_7"] / (out["f_pair_count_30"] + 1.0)
    )
    out["f_item_recent_rate"] = (
        out["f_item_count_7"] / (out["f_item_count_30"] + 1.0)
    )
    out["f_pair_recency_score"] = np.exp(
        -out["f_pair_recency"].clip(lower=0) / 30.0
    ) * (out["f_pair_count"] > 0).astype(float)

    for src in (
        "raw_u_age", "raw_u_active", "raw_u_club_member_status",
        "raw_u_fn", "raw_i_product_code", "raw_i_product_type_no",
        "raw_i_section_no", "raw_i_garment_group_no"
    ):
        out["f_" + src[4:]] = X[src].to_numpy()

    return out.astype(float)
