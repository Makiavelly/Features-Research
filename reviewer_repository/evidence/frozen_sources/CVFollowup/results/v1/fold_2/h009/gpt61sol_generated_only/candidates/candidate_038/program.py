import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_pair_count_7d", "f_pair_count_30d", "f_pair_count_90d",
        "f_pair_recency", "f_customer_count_30d", "f_customer_count_90d",
        "f_customer_recency", "f_item_count_7d", "f_item_count_30d",
        "f_item_count_90d", "f_item_recency", "f_pair_decay",
        "f_customer_decay", "f_item_decay", "f_affinity_type_30d",
        "f_affinity_department_30d", "f_affinity_garment_30d",
        "f_affinity_colour_30d", "f_affinity_section_30d",
        "f_affinity_product_30d", "f_item_channel1_share_30d",
        "f_pair_share_customer_30d", "f_pair_share_item_30d",
        "f_category_share_customer_30d", "f_item_trend_7_30d",
        "f_pair_trend_7_30d", "f_item_customers_30d",
        "f_affinity_type_7d", "f_affinity_product_90d",
        "f_customer_trend_7_30d", "f_item_trend_30_90d",
        "f_department_share_customer_30d"
    ]
    out = pd.DataFrame(index=X.index)
    if len(history) == 0:
        for n in names:
            out[n] = 0.0
        return out

    h = history
    d = h["days_ago"].astype(float)
    customer = X["customer_id"]
    article = X["article_id"]
    pi = pd.MultiIndex.from_arrays([customer.to_numpy(), article.to_numpy()])

    def size(frame, keys):
        return frame.groupby(keys, sort=False).size()

    r7 = h.loc[d <= 7]
    r30 = h.loc[d <= 30]
    r90 = h.loc[d <= 90]
    p7 = size(r7, ["customer_id", "article_id"])
    p30 = size(r30, ["customer_id", "article_id"])
    p90 = size(r90, ["customer_id", "article_id"])
    c7 = size(r7, "customer_id")
    c30 = size(r30, "customer_id")
    c90 = size(r90, "customer_id")
    i7 = size(r7, "article_id")
    i30 = size(r30, "article_id")
    i90 = size(r90, "article_id")

    pc7 = p7.reindex(pi).fillna(0).to_numpy()
    pc30 = p30.reindex(pi).fillna(0).to_numpy()
    out["f_pair_count_7d"] = pc7
    out["f_pair_count_30d"] = pc30
    out["f_pair_count_90d"] = p90.reindex(pi).fillna(0).to_numpy()
    out["f_pair_recency"] = h.groupby(
        ["customer_id", "article_id"], sort=False
    )["days_ago"].min().reindex(pi).to_numpy()

    cc7 = customer.map(c7).fillna(0).to_numpy()
    cc30 = customer.map(c30).fillna(0).to_numpy()
    out["f_customer_count_30d"] = cc30
    out["f_customer_count_90d"] = customer.map(c90).fillna(0)
    out["f_customer_recency"] = customer.map(
        h.groupby("customer_id", sort=False)["days_ago"].min()
    )

    ic7 = article.map(i7).fillna(0).to_numpy()
    ic30 = article.map(i30).fillna(0).to_numpy()
    ic90 = article.map(i90).fillna(0).to_numpy()
    out["f_item_count_7d"] = ic7
    out["f_item_count_30d"] = ic30
    out["f_item_count_90d"] = ic90
    out["f_item_recency"] = article.map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    )

    weight = pd.Series(np.exp(-d.to_numpy() / 30.0), index=h.index)
    out["f_pair_decay"] = weight.groupby(
        [h["customer_id"], h["article_id"]], sort=False
    ).sum().reindex(pi).fillna(0).to_numpy()
    out["f_customer_decay"] = customer.map(
        weight.groupby(h["customer_id"], sort=False).sum()
    ).fillna(0)
    out["f_item_decay"] = article.map(
        weight.groupby(h["article_id"], sort=False).sum()
    ).fillna(0)

    def affinity(frame, hcol, xcol):
        s = size(frame, ["customer_id", hcol])
        ix = pd.MultiIndex.from_arrays([
            customer.to_numpy(), X[xcol].to_numpy()
        ])
        return s.reindex(ix).fillna(0).to_numpy()

    typ30 = affinity(r30, "product_type_no", "raw_i_product_type_no")
    dep30 = affinity(r30, "department_no", "raw_i_department_no")
    out["f_affinity_type_30d"] = typ30
    out["f_affinity_department_30d"] = dep30
    out["f_affinity_garment_30d"] = affinity(r30, "garment_group_no", "raw_i_garment_group_no")
    out["f_affinity_colour_30d"] = affinity(r30, "colour_group_code", "raw_i_colour_group_code")
    out["f_affinity_section_30d"] = affinity(r30, "section_no", "raw_i_section_no")
    out["f_affinity_product_30d"] = affinity(r30, "product_code", "raw_i_product_code")
    out["f_affinity_type_7d"] = affinity(r7, "product_type_no", "raw_i_product_type_no")
    out["f_affinity_product_90d"] = affinity(r90, "product_code", "raw_i_product_code")

    out["f_item_channel1_share_30d"] = article.map(
        r30.assign(z=(r30["sales_channel_id"] == 1).astype(float)).groupby(
            "article_id", sort=False
        )["z"].mean()
    )

    out["f_pair_share_customer_30d"] = pc30 / np.maximum(cc30, 1.0)
    out["f_pair_share_item_30d"] = pc30 / np.maximum(ic30, 1.0)
    out["f_category_share_customer_30d"] = typ30 / np.maximum(cc30, 1.0)
    out["f_item_trend_7_30d"] = ic7 / np.maximum(ic30, 1.0)
    out["f_pair_trend_7_30d"] = pc7 / np.maximum(pc30, 1.0)
    out["f_item_customers_30d"] = article.map(
        r30.groupby("article_id", sort=False)["customer_id"].nunique()
    ).fillna(0)
    out["f_customer_trend_7_30d"] = cc7 / np.maximum(cc30, 1.0)
    out["f_item_trend_30_90d"] = ic30 / np.maximum(ic90, 1.0)
    out["f_department_share_customer_30d"] = dep30 / np.maximum(cc30, 1.0)

    return out[names].astype(float)
