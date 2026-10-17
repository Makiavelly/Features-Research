import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_pair_count", "f_pair_count_30d", "f_pair_recency",
        "f_item_count_7d", "f_item_count_30d", "f_item_count_90d",
        "f_item_count_all", "f_item_trend", "f_item_customers",
        "f_user_count_7d", "f_user_count_30d", "f_user_count_all",
        "f_user_recency", "f_user_section_count", "f_user_type_count",
        "f_user_colour_count", "f_user_avg_price", "f_item_avg_price",
        "f_pair_avg_price", "f_price_affinity",
        "f_item_channel2_share", "f_user_channel2_share",
        "f_i_product", "f_i_type", "f_i_section", "f_i_department",
        "f_i_colour", "f_i_colour_master", "f_u_age", "f_u_active",
        "f_u_club", "f_u_fn"
    ]
    out = pd.DataFrame(index=X.index)
    if history is None or len(history) == 0:
        for c in names:
            out[c] = np.nan
        return out

    h = history
    d = pd.to_numeric(h["days_ago"], errors="coerce").fillna(10**6)
    xuid = X["customer_id"]
    xaid = X["article_id"]

    def k(a, b):
        return a.astype(str) + "\x1e" + b.astype(str)

    pair = k(h["customer_id"], h["article_id"])
    xpair = k(xuid, xaid)
    usec = k(h["customer_id"], h["section_no"])
    xusec = k(xuid, X["raw_i_section_no"])
    uset = k(h["customer_id"], h["product_type_no"])
    xuset = k(xuid, X["raw_i_product_type_no"])
    ucol = k(h["customer_id"], h["colour_group_code"])
    xucol = k(xuid, X["raw_i_colour_group_code"])

    def count(mask, key, xkey):
        z = h.loc[mask]
        if len(z) == 0:
            return pd.Series(np.nan, index=X.index)
        s = pd.Series(1, index=z.index).groupby(key.loc[z.index]).sum()
        return xkey.map(s)

    allm = np.ones(len(h), dtype=bool)
    m7, m30, m90 = d <= 7, d <= 30, d <= 90

    out["f_pair_count"] = count(allm, pair, xpair).fillna(0)
    out["f_pair_count_30d"] = count(m30, pair, xpair).fillna(0)
    pr = d.groupby(pair).min()
    out["f_pair_recency"] = xpair.map(pr)

    for nm, mask in [("7d", m7), ("30d", m30), ("90d", m90), ("all", allm)]:
        out["f_item_count_" + nm] = count(mask, h["article_id"], xaid).fillna(0)

    i7 = count(m7, h["article_id"], xaid).fillna(0)
    i90 = count(m90, h["article_id"], xaid).fillna(0)
    ia = count(allm, h["article_id"], xaid).fillna(0)
    out["f_item_trend"] = (i7 + 1.0) / (i90 / 13.0 + 1.0)

    ic = h.groupby("article_id")["customer_id"].nunique()
    out["f_item_customers"] = xaid.map(ic).fillna(0)

    for nm, mask in [("7d", m7), ("30d", m30), ("all", allm)]:
        out["f_user_count_" + nm] = count(mask, h["customer_id"], xuid).fillna(0)

    out["f_user_recency"] = xuid.map(h.groupby("customer_id")["days_ago"].min())
    out["f_user_section_count"] = count(m90, usec, xusec).fillna(0)
    out["f_user_type_count"] = count(m90, uset, xuset).fillna(0)
    out["f_user_colour_count"] = count(m90, ucol, xucol).fillna(0)

    price = pd.to_numeric(h["price"], errors="coerce")
    pmean_u = h.assign(_p=price).groupby("customer_id")["_p"].mean()
    pmean_i = h.assign(_p=price).groupby("article_id")["_p"].mean()
    pmean_pair = h.assign(_p=price).groupby(pair)["_p"].mean()
    xp = pd.to_numeric(X["raw_i_product_code"], errors="coerce")
    out["f_user_avg_price"] = xuid.map(pmean_u)
    out["f_item_avg_price"] = xaid.map(pmean_i)
    out["f_pair_avg_price"] = xpair.map(pmean_pair)
    out["f_price_affinity"] = out["f_pair_avg_price"] / (out["f_user_avg_price"] + 1e-6)

    ch = pd.to_numeric(h["sales_channel_id"], errors="coerce")
    c2 = h.assign(_c=ch).groupby("article_id")["_c"].mean()
    u2 = h.assign(_c=(ch == 2).astype(float)).groupby("customer_id")["_c"].mean()
    out["f_item_channel2_share"] = xaid.map(c2)
    out["f_user_channel2_share"] = xuid.map(u2)

    out["f_i_product"] = xp
    out["f_i_type"] = pd.to_numeric(X["raw_i_product_type_no"], errors="coerce")
    out["f_i_section"] = pd.to_numeric(X["raw_i_section_no"], errors="coerce")
    out["f_i_department"] = pd.to_numeric(X["raw_i_department_no"], errors="coerce")
    out["f_i_colour"] = pd.to_numeric(X["raw_i_colour_group_code"], errors="coerce")
    out["f_i_colour_master"] = pd.to_numeric(X["raw_i_perceived_colour_master_id"], errors="coerce")
    out["f_u_age"] = pd.to_numeric(X["raw_u_age"], errors="coerce")
    out["f_u_active"] = pd.to_numeric(X["raw_u_active"], errors="coerce")
    out["f_u_club"] = pd.to_numeric(X["raw_u_club_member_status"], errors="coerce")
    out["f_u_fn"] = pd.to_numeric(X["raw_u_fn"], errors="coerce")
    return out.replace([np.inf, -np.inf], np.nan)
