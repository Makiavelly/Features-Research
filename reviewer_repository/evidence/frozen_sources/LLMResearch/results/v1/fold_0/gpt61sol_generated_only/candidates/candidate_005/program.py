import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)

    def smap(key, value=None, window=None, minimum=False):
        h = history if window is None else history.loc[history["days_ago"] <= window]
        if value is None:
            s = h.groupby(key).size()
        elif minimum:
            s = h.groupby(key)[value].min()
        else:
            s = h.groupby(key)[value].mean()
        return X[key].map(s).fillna(0).to_numpy()

    def pmap(hkeys, xkeys, window=None, minimum=False):
        h = history if window is None else history.loc[history["days_ago"] <= window]
        g = h.groupby(hkeys)
        s = g["days_ago"].min() if minimum else g.size()
        idx = pd.MultiIndex.from_arrays(
            [X[k].to_numpy() for k in xkeys], names=hkeys
        )
        return s.reindex(idx).fillna(0).to_numpy()

    out["f_item_7"] = smap("article_id", window=7)
    out["f_item_30"] = smap("article_id", window=30)
    out["f_item_all"] = smap("article_id")
    out["f_item_recency"] = smap("article_id", "days_ago", minimum=True)

    out["f_user_7"] = smap("customer_id", window=7)
    out["f_user_30"] = smap("customer_id", window=30)
    out["f_user_all"] = smap("customer_id")
    out["f_user_recency"] = smap("customer_id", "days_ago", minimum=True)

    out["f_pair_30"] = pmap(
        ["customer_id", "article_id"],
        ["customer_id", "article_id"], 30
    )
    out["f_pair_all"] = pmap(
        ["customer_id", "article_id"],
        ["customer_id", "article_id"]
    )
    out["f_pair_recency"] = pmap(
        ["customer_id", "article_id"],
        ["customer_id", "article_id"], minimum=True
    )

    cats = [
        ("product_code", "raw_i_product_code"),
        ("product_type_no", "raw_i_product_type_no"),
        ("department_no", "raw_i_department_no"),
        ("section_no", "raw_i_section_no"),
    ]
    for i, (hk, xk) in enumerate(cats):
        out["f_affinity_%d_30" % i] = pmap(
            ["customer_id", hk], ["customer_id", xk], 30
        )
        out["f_affinity_%d_all" % i] = pmap(
            ["customer_id", hk], ["customer_id", xk]
        )
        out["f_category_%d_30" % i] = pmap(
            ["article_id", hk], ["article_id", xk], 30
        )

    out["f_age"] = X["raw_u_age"].to_numpy()
    out["f_active"] = X["raw_u_active"].to_numpy()
    out["f_club"] = X["raw_u_club_member_status"].to_numpy()
    out["f_product"] = X["raw_i_product_code"].to_numpy()
    out["f_type"] = X["raw_i_product_type_no"].to_numpy()
    out["f_department"] = X["raw_i_department_no"].to_numpy()
    out["f_section"] = X["raw_i_section_no"].to_numpy()

    out["f_item_recent_ratio"] = out["f_item_7"] / (out["f_item_30"] + 1.0)
    out["f_user_recent_ratio"] = out["f_user_7"] / (out["f_user_30"] + 1.0)
    out["f_pair_user_share"] = out["f_pair_all"] / (out["f_user_all"] + 1.0)

    return out.replace([np.inf, -np.inf], np.nan)
