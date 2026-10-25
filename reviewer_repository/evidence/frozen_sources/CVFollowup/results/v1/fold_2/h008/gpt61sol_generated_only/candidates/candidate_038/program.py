import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    feature_names = [
        "f_pair_30d", "f_pair_90d", "f_pair_all", "f_pair_recency",
        "f_pair_decay", "f_customer_30d", "f_customer_all",
        "f_customer_recency", "f_customer_decay", "f_item_7d",
        "f_item_30d", "f_item_90d", "f_item_recency", "f_item_decay",
        "f_type_pop_30d", "f_customer_type_90d",
        "f_customer_section_90d", "f_customer_garment_90d",
        "f_customer_colour_90d", "f_user_age", "f_user_fn",
        "f_user_active", "f_user_member", "f_item_type",
        "f_item_section", "f_item_garment"
    ]

    if history is None or len(history) == 0:
        for name in feature_names:
            if name == "f_user_age":
                value = pd.to_numeric(X["raw_u_age"], errors="coerce")
            elif name == "f_user_fn":
                value = pd.to_numeric(X["raw_u_fn"], errors="coerce")
            elif name == "f_user_active":
                value = pd.to_numeric(X["raw_u_active"], errors="coerce")
            elif name == "f_user_member":
                value = pd.to_numeric(X["raw_u_club_member_status"], errors="coerce")
            elif name == "f_item_type":
                value = pd.to_numeric(X["raw_i_product_type_no"], errors="coerce")
            elif name == "f_item_section":
                value = pd.to_numeric(X["raw_i_section_no"], errors="coerce")
            elif name == "f_item_garment":
                value = pd.to_numeric(X["raw_i_garment_group_no"], errors="coerce")
            else:
                value = np.zeros(len(X), dtype=float)
            out[name] = np.asarray(value)
        return out.astype(float)

    h = history.reset_index(drop=True)
    days = pd.to_numeric(h["days_ago"], errors="coerce")
    customer = X["customer_id"]
    article = X["article_id"]

    def key(left, right):
        return (
            left.astype("string").fillna("<na>") + "|" +
            right.astype("string").fillna("<na>")
        )

    pair_h = key(h["customer_id"], h["article_id"])
    pair_x = key(customer, article)
    decay = np.exp(-days.astype(float) / 30.0)

    def mapped_count(hist_key, candidate_key, mask=None):
        if mask is None:
            stat = h.groupby(hist_key, sort=False).size()
        else:
            stat = h.loc[mask].groupby(hist_key.loc[mask], sort=False).size()
        return candidate_key.map(stat).fillna(0).to_numpy()

    m7 = days <= 7
    m30 = days <= 30
    m90 = days <= 90

    out["f_pair_30d"] = mapped_count(pair_h, pair_x, m30)
    out["f_pair_90d"] = mapped_count(pair_h, pair_x, m90)
    out["f_pair_all"] = mapped_count(pair_h, pair_x)
    out["f_pair_recency"] = pair_x.map(
        h.groupby(pair_h, sort=False)["days_ago"].min()
    ).to_numpy()
    out["f_pair_decay"] = pair_x.map(
        decay.groupby(pair_h, sort=False).sum()
    ).fillna(0).to_numpy()

    out["f_customer_30d"] = mapped_count(h["customer_id"], customer, m30)
    out["f_customer_all"] = mapped_count(h["customer_id"], customer)
    out["f_customer_recency"] = customer.map(
        h.groupby("customer_id", sort=False)["days_ago"].min()
    ).to_numpy()
    out["f_customer_decay"] = customer.map(
        decay.groupby(h["customer_id"], sort=False).sum()
    ).fillna(0).to_numpy()

    out["f_item_7d"] = mapped_count(h["article_id"], article, m7)
    out["f_item_30d"] = mapped_count(h["article_id"], article, m30)
    out["f_item_90d"] = mapped_count(h["article_id"], article, m90)
    out["f_item_recency"] = article.map(
        h.groupby("article_id", sort=False)["days_ago"].min()
    ).to_numpy()
    out["f_item_decay"] = article.map(
        decay.groupby(h["article_id"], sort=False).sum()
    ).fillna(0).to_numpy()

    out["f_type_pop_30d"] = X["raw_i_product_type_no"].map(
        h.loc[m30].groupby("product_type_no", sort=False).size()
    ).fillna(0).to_numpy()

    recent = h.loc[m90]
    for raw_col, hist_col, out_col in (
        ("raw_i_product_type_no", "product_type_no", "f_customer_type_90d"),
        ("raw_i_section_no", "section_no", "f_customer_section_90d"),
        ("raw_i_garment_group_no", "garment_group_no", "f_customer_garment_90d"),
        ("raw_i_colour_group_code", "colour_group_code", "f_customer_colour_90d"),
    ):
        hist_key = key(recent["customer_id"], recent[hist_col])
        candidate_key = key(customer, X[raw_col])
        out[out_col] = candidate_key.map(
            recent.groupby(hist_key, sort=False).size()
        ).fillna(0).to_numpy()

    out["f_user_age"] = pd.to_numeric(X["raw_u_age"], errors="coerce").to_numpy()
    out["f_user_fn"] = pd.to_numeric(X["raw_u_fn"], errors="coerce").to_numpy()
    out["f_user_active"] = pd.to_numeric(X["raw_u_active"], errors="coerce").to_numpy()
    out["f_user_member"] = pd.to_numeric(
        X["raw_u_club_member_status"], errors="coerce"
    ).to_numpy()
    out["f_item_type"] = pd.to_numeric(
        X["raw_i_product_type_no"], errors="coerce"
    ).to_numpy()
    out["f_item_section"] = pd.to_numeric(
        X["raw_i_section_no"], errors="coerce"
    ).to_numpy()
    out["f_item_garment"] = pd.to_numeric(
        X["raw_i_garment_group_no"], errors="coerce"
    ).to_numpy()

    return out.astype(float)
