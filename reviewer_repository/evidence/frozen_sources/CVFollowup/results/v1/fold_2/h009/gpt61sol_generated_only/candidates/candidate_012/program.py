import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    names = [
        "f_pair_count_7d", "f_pair_count_30d", "f_pair_count_90d",
        "f_pair_count_180d", "f_pair_recency", "f_customer_count_7d",
        "f_customer_count_30d", "f_customer_count_90d", "f_customer_recency",
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_count_180d", "f_item_recency", "f_pair_decay",
        "f_customer_decay", "f_item_decay", "f_affinity_type_30d",
        "f_affinity_department_30d", "f_affinity_garment_30d",
        "f_affinity_colour_30d", "f_affinity_section_30d",
        "f_item_channel1_share_30d", "f_pair_price_mean",
        "f_item_price_mean", "f_customer_price_mean", "f_pair_price_last",
        "f_customer_age_match", "f_raw_product_code", "f_raw_product_type",
        "f_raw_department", "f_raw_section", "f_raw_garment", "f_raw_colour"
    ]
    if len(history) == 0:
        for n in names:
            out[n] = 0.0
        return out

    h = history
    d = h["days_ago"].astype(float)
    pi = pd.MultiIndex.from_arrays([
        X["customer_id"].to_numpy(), X["article_id"].to_numpy()
    ])

    def sizes(frame, keys):
        return frame.groupby(keys, sort=False).size()

    for w in (7, 30, 90, 180):
        s = sizes(h.loc[d <= w], ["customer_id", "article_id"])
        out["f_pair_count_%dd" % w] = s.reindex(pi).fillna(0).to_numpy()

    out["f_pair_recency"] = h.groupby(
        ["customer_id", "article_id"], sort=False
    )["days_ago"].min().reindex(pi).to_numpy()

    for w in (7, 30, 90):
        out["f_customer_count_%dd" % w] = X["customer_id"].map(
            sizes(h.loc[d <= w], "customer_id")
        ).fillna(0)

    out["f_customer_recency"] = X["customer_id"].map(
        h.groupby("customer_id", sort=False)["days_ago"].min()
    )

    for w in (7, 30, 90, 180):
        out["f_item_count_%dd" % w] = X["article_id"].map(
            sizes(h.loc[d <= w], "article_id")
        ).fillna(0)

    out["f_item_recency"] = X["article_id"].map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    )

    wt = pd.Series(np.exp(-d.to_numpy() / 30.0), index=h.index)
    out["f_pair_decay"] = wt.groupby(
        [h["customer_id"], h["article_id"]], sort=False
    ).sum().reindex(pi).fillna(0).to_numpy()
    out["f_customer_decay"] = X["customer_id"].map(
        wt.groupby(h["customer_id"], sort=False).sum()
    ).fillna(0)
    out["f_item_decay"] = X["article_id"].map(
        wt.groupby(h["article_id"], sort=False).sum()
    ).fillna(0)

    r = h.loc[d <= 30]

    def affinity(hc, xc):
        s = sizes(r, ["customer_id", hc])
        ix = pd.MultiIndex.from_arrays([
            X["customer_id"].to_numpy(), X[xc].to_numpy()
        ])
        return s.reindex(ix).fillna(0).to_numpy()

    out["f_affinity_type_30d"] = affinity("product_type_no", "raw_i_product_type_no")
    out["f_affinity_department_30d"] = affinity("department_no", "raw_i_department_no")
    out["f_affinity_garment_30d"] = affinity("garment_group_no", "raw_i_garment_group_no")
    out["f_affinity_colour_30d"] = affinity("colour_group_code", "raw_i_colour_group_code")
    out["f_affinity_section_30d"] = affinity("section_no", "raw_i_section_no")

    out["f_item_channel1_share_30d"] = X["article_id"].map(
        r.groupby("article_id", sort=False)["sales_channel_id"].apply(
            lambda z: (z == 1).mean()
        )
    )

    pair_price = h.groupby(["customer_id", "article_id"], sort=False)["price"]
    out["f_pair_price_mean"] = pair_price.mean().reindex(pi).to_numpy()
    out["f_pair_price_last"] = h.sort_values("days_ago").groupby(
        ["customer_id", "article_id"], sort=False
    )["price"].first().reindex(pi).to_numpy()
    out["f_item_price_mean"] = X["article_id"].map(
        h.groupby("article_id", sort=False)["price"].mean()
    )
    out["f_customer_price_mean"] = X["customer_id"].map(
        h.groupby("customer_id", sort=False)["price"].mean()
    )

    age = h.groupby("customer_id", sort=False)["customer_age"].last()
    out["f_customer_age_match"] = X["customer_id"].map(age) - X["raw_u_age"]

    out["f_raw_product_code"] = X["raw_i_product_code"]
    out["f_raw_product_type"] = X["raw_i_product_type_no"]
    out["f_raw_department"] = X["raw_i_department_no"]
    out["f_raw_section"] = X["raw_i_section_no"]
    out["f_raw_garment"] = X["raw_i_garment_group_no"]
    out["f_raw_colour"] = X["raw_i_colour_group_code"]

    return out.astype(float)
