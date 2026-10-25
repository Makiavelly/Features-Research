import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_item_pop_7", "f_item_pop_30", "f_item_pop_all", "f_item_pop_decay",
        "f_item_recency", "f_item_trend", "f_pair_count", "f_pair_count_30",
        "f_pair_decay", "f_pair_recency", "f_customer_count_7",
        "f_customer_count_30", "f_customer_recency", "f_customer_recency_90",
        "f_type_affinity_30", "f_department_affinity_30",
        "f_section_affinity_30", "f_product_affinity_30", "f_type_pop_7",
        "f_department_pop_7", "f_section_pop_7", "f_product_pop_7",
        "f_item_price", "f_item_price_30", "f_customer_department_price",
        "f_customer_channel2", "f_u_age", "f_i_product_type",
        "f_i_department", "f_i_section", "f_i_garment_group",
        "f_i_index_group"
    ]
    out = pd.DataFrame(index=X.index)
    static = {
        "f_u_age": "raw_u_age",
        "f_i_product_type": "raw_i_product_type_no",
        "f_i_department": "raw_i_department_no",
        "f_i_section": "raw_i_section_no",
        "f_i_garment_group": "raw_i_garment_group_no",
        "f_i_index_group": "raw_i_index_group_no"
    }
    if history is None or len(history) == 0:
        for n in names:
            if n in static:
                out[n] = X[static[n]].to_numpy()
            elif n.endswith("recency"):
                out[n] = 4000.0
            else:
                out[n] = 0.0
        return out

    h = history
    r7 = h.loc[h["days_ago"] <= 7]
    r30 = h.loc[h["days_ago"] <= 30]
    r90 = h.loc[h["days_ago"] <= 90]
    u = X["customer_id"]
    a = X["article_id"]

    def one(s, key, fill=0.0):
        return key.map(s).fillna(fill).to_numpy(dtype=float)

    def two(s, k1, k2, fill=0.0):
        ix = pd.MultiIndex.from_arrays([k1.to_numpy(), k2.to_numpy()])
        return s.reindex(ix).fillna(fill).to_numpy(dtype=float)

    def cnt(frame, keys):
        return frame.groupby(keys, observed=True).size()

    i7 = cnt(r7, "article_id")
    i30 = cnt(r30, "article_id")
    iall = cnt(h, "article_id")
    decay = h.assign(_w=np.exp(-h["days_ago"].clip(lower=0) / 14.0))
    idecay = decay.groupby("article_id", observed=True)["_w"].sum()
    out["f_item_pop_7"] = np.log1p(one(i7, a))
    out["f_item_pop_30"] = np.log1p(one(i30, a))
    out["f_item_pop_all"] = np.log1p(one(iall, a))
    out["f_item_pop_decay"] = np.log1p(one(idecay, a))
    out["f_item_recency"] = one(
        h.groupby("article_id", observed=True)["days_ago"].min(), a, 4000
    )
    out["f_item_trend"] = one(i7, a) / np.maximum(one(i30, a), 1.0)

    pair = h.groupby(["customer_id", "article_id"], observed=True).agg(
        n=("days_ago", "size"), rec=("days_ago", "min")
    )
    pdecay = decay.groupby(["customer_id", "article_id"], observed=True)["_w"].sum()
    out["f_pair_count"] = np.log1p(two(pair["n"], u, a))
    out["f_pair_count_30"] = np.log1p(
        two(cnt(r30, ["customer_id", "article_id"]), u, a)
    )
    out["f_pair_decay"] = two(pdecay, u, a)
    out["f_pair_recency"] = two(pair["rec"], u, a, 4000)

    c7 = cnt(r7, "customer_id")
    c30 = cnt(r30, "customer_id")
    out["f_customer_count_7"] = np.log1p(one(c7, u))
    out["f_customer_count_30"] = np.log1p(one(c30, u))
    out["f_customer_recency"] = one(
        h.groupby("customer_id", observed=True)["days_ago"].min(), u, 4000
    )
    out["f_customer_recency_90"] = one(
        r90.groupby("customer_id", observed=True)["days_ago"].min(), u, 4000
    )

    fields = [
        ("product_type_no", "raw_i_product_type_no", "type"),
        ("department_no", "raw_i_department_no", "department"),
        ("section_no", "raw_i_section_no", "section"),
        ("product_code", "raw_i_product_code", "product")
    ]
    den = np.maximum(one(c30, u), 1.0)
    for field, raw, label in fields:
        hit = two(cnt(r30, ["customer_id", field]), u, X[raw])
        out["f_" + label + "_affinity_30"] = hit / den
        out["f_" + label + "_pop_7"] = np.log1p(
            one(cnt(r7, field), X[raw])
        )

    out["f_item_price"] = one(
        h.groupby("article_id", observed=True)["price"].mean(), a, np.nan
    )
    out["f_item_price_30"] = one(
        r30.groupby("article_id", observed=True)["price"].mean(), a, np.nan
    )
    out["f_customer_department_price"] = two(
        h.groupby(["customer_id", "department_no"], observed=True)["price"].mean(),
        u, X["raw_i_department_no"], np.nan
    )
    ch = h.assign(_ch=(h["sales_channel_id"] == 2).astype(float))
    out["f_customer_channel2"] = one(
        ch.groupby("customer_id", observed=True)["_ch"].mean(), u
    )

    for name, col in static.items():
        out[name] = X[col].to_numpy()

    return out.reindex(columns=names).replace([np.inf, -np.inf], np.nan)
