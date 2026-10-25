import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    c = X["customer_id"].to_numpy()
    a = X["article_id"].to_numpy()
    pairkey = pd.MultiIndex.from_arrays([c, a])

    def pmap(h, name):
        if len(h):
            s = h.groupby(["customer_id", "article_id"], sort=False).size()
            out[name] = s.reindex(pairkey).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    def cmap(h, name):
        if len(h):
            s = h.groupby("customer_id", sort=False).size()
            out[name] = X["customer_id"].map(s).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    def imap(h, name):
        if len(h):
            s = h.groupby("article_id", sort=False).size()
            out[name] = X["article_id"].map(s).fillna(0).to_numpy()
        else:
            out[name] = 0.0

    h14 = history.loc[history["days_ago"] <= 14]
    h60 = history.loc[history["days_ago"] <= 60]
    h180 = history.loc[history["days_ago"] <= 180]

    pmap(h14, "f_pair_14d")
    pmap(h60, "f_pair_60d")
    pmap(h180, "f_pair_180d")
    cmap(h14, "f_customer_14d")
    cmap(h60, "f_customer_60d")
    cmap(h180, "f_customer_180d")
    imap(h14, "f_article_14d")
    imap(h60, "f_article_60d")
    imap(h180, "f_article_180d")

    if len(history):
        pg = history.groupby(["customer_id", "article_id"], sort=False)
        pairrec = pg["days_ago"].min().reindex(pairkey)
        out["f_pair_recency"] = pairrec.to_numpy()
        out["f_pair_decay_14"] = np.exp(
            -pairrec.to_numpy(dtype=float) / 14.0
        )

        wh = history.assign(
            _w=np.exp(-history["days_ago"].to_numpy(dtype=float) / 45.0)
        )
        out["f_pair_decay_45"] = wh.groupby(
            ["customer_id", "article_id"], sort=False
        )["_w"].sum().reindex(pairkey).fillna(0).to_numpy()

        cr = history.groupby("customer_id", sort=False)["days_ago"].min()
        out["f_customer_recency"] = X["customer_id"].map(cr).to_numpy()

        p60 = h60.groupby(
            ["customer_id", "article_id"], sort=False
        ).size().reindex(pairkey).fillna(0).to_numpy(dtype=float)
        cu60 = X["customer_id"].map(
            h60.groupby("customer_id", sort=False).size()
        ).fillna(0).to_numpy(dtype=float)
        ai60 = X["article_id"].map(
            h60.groupby("article_id", sort=False).size()
        ).fillna(0).to_numpy(dtype=float)
        out["f_pair_customer_fraction"] = p60 / np.maximum(cu60, 1.0)
        out["f_pair_article_fraction"] = p60 / np.maximum(ai60, 1.0)

        for raw, col, name in [
            ("raw_i_product_type_no", "product_type_no", "f_customer_type_60d"),
            ("raw_i_department_no", "department_no", "f_customer_department_60d"),
            ("raw_i_section_no", "section_no", "f_customer_section_60d"),
            ("raw_i_colour_group_code", "colour_group_code", "f_customer_colour_60d"),
        ]:
            k = pd.MultiIndex.from_arrays([c, X[raw].to_numpy()])
            s = h180.groupby(["customer_id", col], sort=False).size()
            out[name] = s.reindex(k).fillna(0).to_numpy()

        for raw, col, name in [
            ("raw_i_product_type_no", "product_type_no", "f_type_popularity_14d"),
            ("raw_i_department_no", "department_no", "f_department_popularity_14d"),
            ("raw_i_section_no", "section_no", "f_section_popularity_14d"),
            ("raw_i_colour_group_code", "colour_group_code", "f_colour_popularity_14d"),
        ]:
            s = h14.groupby(col, sort=False).size()
            out[name] = X[raw].map(s).fillna(0).to_numpy()

        out["f_article_customers"] = X["article_id"].map(
            history.groupby("article_id", sort=False)["customer_id"].nunique()
        ).fillna(0).to_numpy()
        out["f_customer_articles"] = X["customer_id"].map(
            history.groupby("customer_id", sort=False)["article_id"].nunique()
        ).fillna(0).to_numpy()
    else:
        for name in [
            "f_pair_recency", "f_pair_decay_14", "f_pair_decay_45",
            "f_customer_recency", "f_pair_customer_fraction",
            "f_pair_article_fraction", "f_customer_type_60d",
            "f_customer_department_60d", "f_customer_section_60d",
            "f_customer_colour_60d", "f_type_popularity_14d",
            "f_department_popularity_14d", "f_section_popularity_14d",
            "f_colour_popularity_14d", "f_article_customers",
            "f_customer_articles"
        ]:
            out[name] = 0.0

    for raw, name in [
        ("raw_i_product_code", "f_product_code"),
        ("raw_i_product_type_no", "f_product_type"),
        ("raw_i_department_no", "f_department"),
        ("raw_i_section_no", "f_section"),
        ("raw_i_garment_group_no", "f_garment_group"),
        ("raw_i_colour_group_code", "f_colour_group"),
    ]:
        out[name] = X[raw].to_numpy(dtype=float)

    return out.astype(float)
