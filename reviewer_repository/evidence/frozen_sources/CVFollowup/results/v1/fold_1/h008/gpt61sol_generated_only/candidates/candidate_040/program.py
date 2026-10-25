import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_item_pop_7", "f_item_pop_30", "f_item_pop_90", "f_item_pop_decay",
        "f_item_recency", "f_pair_count", "f_pair_count_30", "f_pair_count_90",
        "f_pair_recency", "f_customer_count_7", "f_customer_count_30",
        "f_customer_count_90", "f_customer_recency", "f_type_affinity_7",
        "f_type_affinity_30", "f_department_affinity_7",
        "f_department_affinity_30", "f_section_affinity_30",
        "f_garment_affinity_30", "f_type_pop_7", "f_department_pop_7",
        "f_section_pop_7", "f_item_price", "f_customer_department_price",
        "f_category_recency", "f_product_code_pop_30", "f_colour_affinity_30",
        "f_item_channel_share", "f_u_age", "f_i_product_type",
        "f_i_department", "f_i_section", "f_i_garment_group",
        "f_i_index_group", "f_i_product_code", "f_i_colour_group"
    ]
    out = pd.DataFrame(index=X.index)
    if history is None or len(history) == 0:
        for n in names:
            if n.endswith("recency"):
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
            elif n == "f_i_product_code":
                out[n] = X["raw_i_product_code"].to_numpy()
            elif n == "f_i_colour_group":
                out[n] = X["raw_i_colour_group_code"].to_numpy()
            else:
                out[n] = 0.0
        return out

    h = history
    c = X["customer_id"]
    a = X["article_id"]
    ix = pd.MultiIndex.from_arrays([c.to_numpy(), a.to_numpy()])

    def one(s, keys, fill=0.0):
        return keys.map(s).fillna(fill).to_numpy(dtype=float)

    def two(s, k1, k2, fill=0.0):
        return s.reindex(pd.MultiIndex.from_arrays(
            [k1.to_numpy(), k2.to_numpy()])).fillna(fill).to_numpy(dtype=float)

    def count(frame, keys):
        return frame.groupby(keys, observed=True).size()

    r7 = h[h.days_ago <= 7]
    r30 = h[h.days_ago <= 30]
    r90 = h[h.days_ago <= 90]

    i7, i30, i90 = count(r7, "article_id"), count(r30, "article_id"), count(r90, "article_id")
    w = h.assign(_w=np.exp(-h.days_ago.to_numpy() / 14.0))
    idec = w.groupby("article_id", observed=True)["_w"].sum()

    out["f_item_pop_7"] = np.log1p(one(i7, a))
    out["f_item_pop_30"] = np.log1p(one(i30, a))
    out["f_item_pop_90"] = np.log1p(one(i90, a))
    out["f_item_pop_decay"] = np.log1p(one(idec, a))
    out["f_item_recency"] = one(h.groupby("article_id", observed=True).days_ago.min(), a, 4000)

    pair = h.groupby(["customer_id", "article_id"], observed=True).days_ago.agg(["size", "min"])
    out["f_pair_count"] = np.log1p(two(pair["size"], c, a))
    out["f_pair_count_30"] = np.log1p(two(count(r30, ["customer_id", "article_id"]), c, a))
    out["f_pair_count_90"] = np.log1p(two(count(r90, ["customer_id", "article_id"]), c, a))
    out["f_pair_recency"] = two(pair["min"], c, a, 4000)

    cu7, cu30, cu90 = count(r7, "customer_id"), count(r30, "customer_id"), count(r90, "customer_id")
    out["f_customer_count_7"] = np.log1p(one(cu7, c))
    out["f_customer_count_30"] = np.log1p(one(cu30, c))
    out["f_customer_count_90"] = np.log1p(one(cu90, c))
    out["f_customer_recency"] = one(h.groupby("customer_id", observed=True).days_ago.min(), c, 4000)

    total7, total30 = one(cu7, c), one(cu30, c)
    for field, raw, n7, n30 in [
        ("product_type_no", "raw_i_product_type_no", "f_type_affinity_7", "f_type_affinity_30"),
        ("department_no", "raw_i_department_no", "f_department_affinity_7", "f_department_affinity_30"),
    ]:
        out[n7] = two(count(r7, ["customer_id", field]), c, X[raw]) / np.maximum(total7, 1)
        out[n30] = two(count(r30, ["customer_id", field]), c, X[raw]) / np.maximum(total30, 1)

    for field, raw, name in [
        ("section_no", "raw_i_section_no", "f_section_affinity_30"),
        ("garment_group_no", "raw_i_garment_group_no", "f_garment_affinity_30"),
        ("colour_group_code", "raw_i_colour_group_code", "f_colour_affinity_30"),
    ]:
        out[name] = two(count(r30, ["customer_id", field]), c, X[raw]) / np.maximum(total30, 1)

    for field, raw, name in [
        ("product_type_no", "raw_i_product_type_no", "f_type_pop_7"),
        ("department_no", "raw_i_department_no", "f_department_pop_7"),
        ("section_no", "raw_i_section_no", "f_section_pop_7"),
    ]:
        out[name] = np.log1p(one(count(r7, field), X[raw]))

    out["f_item_price"] = one(h.groupby("article_id", observed=True).price.mean(), a, np.nan)
    out["f_customer_department_price"] = two(
        h.groupby(["customer_id", "department_no"], observed=True).price.mean(),
        c, X["raw_i_department_no"], np.nan)
    out["f_category_recency"] = two(
        h.groupby(["customer_id", "product_type_no"], observed=True).days_ago.min(),
        c, X["raw_i_product_type_no"], 4000)
    out["f_product_code_pop_30"] = np.log1p(
        one(count(r30, "product_code"), X["raw_i_product_code"]))
    out["f_item_channel_share"] = one(
        h.groupby("article_id", observed=True).sales_channel_id.mean(), a, np.nan)

    out["f_u_age"] = X["raw_u_age"].to_numpy()
    for name, raw in [
        ("f_i_product_type", "raw_i_product_type_no"),
        ("f_i_department", "raw_i_department_no"),
        ("f_i_section", "raw_i_section_no"),
        ("f_i_garment_group", "raw_i_garment_group_no"),
        ("f_i_index_group", "raw_i_index_group_no"),
        ("f_i_product_code", "raw_i_product_code"),
        ("f_i_colour_group", "raw_i_colour_group_code"),
    ]:
        out[name] = X[raw].to_numpy()
    return out.replace([np.inf, -np.inf], np.nan)
