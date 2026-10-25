import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    names = [
        "f_item_pop_7", "f_item_pop_30", "f_item_pop_decay",
        "f_item_recency", "f_pair_count", "f_pair_count_30",
        "f_pair_recency", "f_customer_count_30", "f_customer_recency",
        "f_type_affinity_30", "f_department_affinity_30",
        "f_section_affinity_30", "f_type_pop_7", "f_department_pop_7",
        "f_item_price", "f_customer_department_price",
        "f_u_age", "f_i_product_type", "f_i_department",
        "f_i_section", "f_i_garment_group", "f_i_index_group"
    ]

    if history is None or len(history) == 0:
        for n in names:
            if n in ("f_item_recency", "f_pair_recency", "f_customer_recency"):
                out[n] = 4000.0
            elif n in ("f_item_price", "f_customer_department_price"):
                out[n] = np.nan
            elif n == "f_u_age":
                out[n] = X["raw_u_age"].to_numpy()
            elif n == "f_i_product_type":
                out[n] = X["raw_i_product_type_no"].to_numpy()
            elif n == "f_i_department":
                out[n] = X["raw_i_department_no"].to_numpy()
            elif n == "f_i_section":
                out[n] = X["raw_i_section_no"].to_numpy()
            elif n == "f_i_garment_group":
                out[n] = X["raw_i_garment_group_no"].to_numpy()
            elif n == "f_i_index_group":
                out[n] = X["raw_i_index_group_no"].to_numpy()
            else:
                out[n] = 0.0
        return out

    h = history
    r7 = h.loc[h["days_ago"] <= 7]
    r30 = h.loc[h["days_ago"] <= 30]
    customer = X["customer_id"]
    article = X["article_id"]

    def one(s, key, fill=0.0):
        return key.map(s).fillna(fill).to_numpy(dtype=float)

    def multi(s, a, b, fill=0.0):
        ix = pd.MultiIndex.from_arrays([a.to_numpy(), b.to_numpy()])
        return s.reindex(ix).fillna(fill).to_numpy(dtype=float)

    def cnt(frame, keys):
        return frame.groupby(keys, observed=True).size()

    item7 = cnt(r7, "article_id")
    item30 = cnt(r30, "article_id")
    itemall = cnt(h, "article_id")
    decay = h.assign(_w=np.exp(-h["days_ago"].clip(lower=0).to_numpy() / 14.0))
    itemdecay = decay.groupby("article_id", observed=True)["_w"].sum()

    out["f_item_pop_7"] = np.log1p(one(item7, article))
    out["f_item_pop_30"] = np.log1p(one(item30, article))
    out["f_item_pop_decay"] = np.log1p(one(itemdecay, article))
    out["f_item_recency"] = one(
        h.groupby("article_id", observed=True)["days_ago"].min(), article, 4000
    )

    pair = h.groupby(["customer_id", "article_id"], observed=True).agg(
        n=("days_ago", "size"), recency=("days_ago", "min")
    )
    out["f_pair_count"] = np.log1p(multi(pair["n"], customer, article))
    out["f_pair_count_30"] = np.log1p(
        multi(cnt(r30, ["customer_id", "article_id"]), customer, article)
    )
    out["f_pair_recency"] = multi(pair["recency"], customer, article, 4000)

    c30 = cnt(r30, "customer_id")
    out["f_customer_count_30"] = np.log1p(one(c30, customer))
    out["f_customer_recency"] = one(
        h.groupby("customer_id", observed=True)["days_ago"].min(), customer, 4000
    )

    total30 = one(c30, customer)
    for field, raw, name in [
        ("product_type_no", "raw_i_product_type_no", "f_type_affinity_30"),
        ("department_no", "raw_i_department_no", "f_department_affinity_30"),
        ("section_no", "raw_i_section_no", "f_section_affinity_30"),
    ]:
        matched = multi(
            cnt(r30, ["customer_id", field]), customer, X[raw]
        )
        out[name] = matched / np.maximum(total30, 1.0)

    out["f_type_pop_7"] = np.log1p(
        one(cnt(r7, "product_type_no"), X["raw_i_product_type_no"])
    )
    out["f_department_pop_7"] = np.log1p(
        one(cnt(r7, "department_no"), X["raw_i_department_no"])
    )

    out["f_item_price"] = one(
        h.groupby("article_id", observed=True)["price"].mean(), article, np.nan
    )
    out["f_customer_department_price"] = multi(
        h.groupby(["customer_id", "department_no"], observed=True)["price"].mean(),
        customer, X["raw_i_department_no"], np.nan
    )

    out["f_u_age"] = X["raw_u_age"].to_numpy()
    out["f_i_product_type"] = X["raw_i_product_type_no"].to_numpy()
    out["f_i_department"] = X["raw_i_department_no"].to_numpy()
    out["f_i_section"] = X["raw_i_section_no"].to_numpy()
    out["f_i_garment_group"] = X["raw_i_garment_group_no"].to_numpy()
    out["f_i_index_group"] = X["raw_i_index_group_no"].to_numpy()

    return out.replace([np.inf, -np.inf], np.nan)
