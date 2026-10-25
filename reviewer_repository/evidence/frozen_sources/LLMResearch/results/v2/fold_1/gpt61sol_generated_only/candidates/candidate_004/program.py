import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    n = len(X)

    def mapped(series, key):
        if len(series) == 0:
            return pd.Series(np.zeros(n), index=X.index)
        return key.map(series).fillna(0).to_numpy()

    def grouped_map(df, cols, value=None, agg="size"):
        if len(df) == 0:
            return {}
        if agg == "size":
            s = df.groupby(cols, sort=False).size()
        else:
            s = df.groupby(cols, sort=False)[value].agg(agg)
        return dict(zip(s.index.tolist(), s.to_numpy()))

    h = history
    c = X["customer_id"]
    a = X["article_id"]

    if len(h):
        ug = h.groupby("customer_id", sort=False)
        ag = h.groupby("article_id", sort=False)

        uc = ug.size()
        ac = ag.size()
        ur = ug["days_ago"].min()
        ar = ag["days_ago"].min()
        ud = ug["article_id"].nunique()
        ad = ag["customer_id"].nunique()

        out["f_customer_count"] = mapped(uc, c)
        out["f_article_count"] = mapped(ac, a)
        out["f_customer_recency"] = c.map(ur).fillna(9999).to_numpy()
        out["f_article_recency"] = a.map(ar).fillna(9999).to_numpy()
        out["f_customer_unique_articles"] = mapped(ud, c)
        out["f_article_unique_customers"] = mapped(ad, a)

        for days, tag in ((7, "7d"), (30, "30d"), (90, "90d")):
            hh = h.loc[h["days_ago"] <= days]
            if len(hh):
                out["f_customer_count_" + tag] = mapped(
                    hh.groupby("customer_id", sort=False).size(), c
                )
                out["f_article_count_" + tag] = mapped(
                    hh.groupby("article_id", sort=False).size(), a
                )
            else:
                out["f_customer_count_" + tag] = 0.0
                out["f_article_count_" + tag] = 0.0

        pair = h.groupby(["customer_id", "article_id"], sort=False)
        pair_n = pair.size()
        pair_r = pair["days_ago"].min()
        keys = pd.Series(list(zip(c.to_numpy(), a.to_numpy())), index=X.index)
        out["f_pair_count"] = keys.map(dict(zip(pair_n.index.tolist(), pair_n.to_numpy()))).fillna(0).to_numpy()
        out["f_pair_recency"] = keys.map(dict(zip(pair_r.index.tolist(), pair_r.to_numpy()))).fillna(9999).to_numpy()

        for days, tag in ((30, "30d"), (90, "90d")):
            hh = h.loc[h["days_ago"] <= days]
            pn = hh.groupby(["customer_id", "article_id"], sort=False).size() if len(hh) else pd.Series(dtype=float)
            out["f_pair_count_" + tag] = keys.map(dict(zip(pn.index.tolist(), pn.to_numpy()))).fillna(0).to_numpy()

        out["f_article_mean_price"] = a.map(ag["price"].mean()).fillna(h["price"].mean()).to_numpy()
        out["f_customer_mean_price"] = c.map(ug["price"].mean()).fillna(h["price"].mean()).to_numpy()

        for raw, hc, tag in (
            ("raw_i_product_code", "product_code", "product"),
            ("raw_i_product_type_no", "product_type_no", "type"),
            ("raw_i_department_no", "department_no", "department"),
            ("raw_i_section_no", "section_no", "section"),
            ("raw_i_garment_group_no", "garment_group_no", "garment"),
        ):
            d = grouped_map(h, ["customer_id", hc])
            k = pd.Series(list(zip(c.to_numpy(), X[raw].to_numpy())), index=X.index)
            out["f_customer_" + tag + "_count"] = k.map(d).fillna(0).to_numpy()

            pop = h.groupby(hc, sort=False).size()
            out["f_" + tag + "_popularity"] = X[raw].map(pop).fillna(0).to_numpy()
    else:
        for name in (
            "f_customer_count", "f_article_count", "f_customer_recency",
            "f_article_recency", "f_customer_unique_articles",
            "f_article_unique_customers", "f_customer_count_7d",
            "f_article_count_7d", "f_customer_count_30d",
            "f_article_count_30d", "f_customer_count_90d",
            "f_article_count_90d", "f_pair_count", "f_pair_recency",
            "f_pair_count_30d", "f_pair_count_90d",
            "f_article_mean_price", "f_customer_mean_price",
            "f_customer_product_count", "f_product_popularity",
            "f_customer_type_count", "f_type_popularity",
            "f_customer_department_count", "f_department_popularity",
            "f_customer_section_count", "f_section_popularity",
            "f_customer_garment_count", "f_garment_popularity"
        ):
            out[name] = 0.0

    out["f_user_age"] = X["raw_u_age"].fillna(-1).to_numpy()
    out["f_user_active"] = X["raw_u_active"].fillna(-1).to_numpy()
    out["f_user_club"] = X["raw_u_club_member_status"].fillna(-1).to_numpy()
    out["f_item_product_code"] = X["raw_i_product_code"].fillna(-1).to_numpy()
    out["f_item_product_type"] = X["raw_i_product_type_no"].fillna(-1).to_numpy()
    out["f_item_department"] = X["raw_i_department_no"].fillna(-1).to_numpy()
    out["f_item_section"] = X["raw_i_section_no"].fillna(-1).to_numpy()
    out["f_item_garment"] = X["raw_i_garment_group_no"].fillna(-1).to_numpy()

    return out
