import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)
    names = [
        "f_item_count_7d", "f_item_count_30d", "f_item_count_all",
        "f_item_recency", "f_customer_count_7d", "f_customer_count_30d",
        "f_customer_count_all", "f_customer_recency", "f_pair_count_all",
        "f_pair_count_30d", "f_pair_recency", "f_customer_product_affinity",
        "f_customer_department_affinity", "f_customer_section_affinity",
        "f_customer_garment_affinity"
    ]
    if history is None or len(history) == 0:
        return pd.DataFrame({k: np.zeros(n, dtype=float) for k in names},
                            index=X.index)

    h = history
    c = X["customer_id"]
    a = X["article_id"]

    h7 = h[h["days_ago"] <= 7]
    h30 = h[h["days_ago"] <= 30]

    out["f_item_count_7d"] = a.map(h7.groupby("article_id").size()).fillna(0)
    out["f_item_count_30d"] = a.map(h30.groupby("article_id").size()).fillna(0)
    out["f_item_count_all"] = a.map(h.groupby("article_id").size()).fillna(0)
    out["f_item_recency"] = a.map(h.groupby("article_id")["days_ago"].min())

    out["f_customer_count_7d"] = c.map(h7.groupby("customer_id").size()).fillna(0)
    out["f_customer_count_30d"] = c.map(h30.groupby("customer_id").size()).fillna(0)
    out["f_customer_count_all"] = c.map(h.groupby("customer_id").size()).fillna(0)
    out["f_customer_recency"] = c.map(
        h.groupby("customer_id")["days_ago"].min()
    )

    hk = h["customer_id"].astype(str) + "|" + h["article_id"].astype(str)
    xk = c.astype(str) + "|" + a.astype(str)
    out["f_pair_count_all"] = xk.map(hk.value_counts()).fillna(0)
    out["f_pair_count_30d"] = xk.map(
        (h30["customer_id"].astype(str) + "|" +
         h30["article_id"].astype(str)).value_counts()
    ).fillna(0)
    out["f_pair_recency"] = xk.map(
        h.assign(_k=hk).groupby("_k")["days_ago"].min()
    )

    for hc, xc, name in [
        ("product_code", "raw_i_product_code", "product"),
        ("department_no", "raw_i_department_no", "department"),
        ("section_no", "raw_i_section_no", "section"),
        ("garment_group_no", "raw_i_garment_group_no", "garment")
    ]:
        kh = h["customer_id"].astype(str) + "|" + h[hc].astype(str)
        kx = c.astype(str) + "|" + X[xc].astype(str)
        out["f_customer_" + name + "_affinity"] = kx.map(
            kh.value_counts()
        ).fillna(0)

    return out.astype(float)
