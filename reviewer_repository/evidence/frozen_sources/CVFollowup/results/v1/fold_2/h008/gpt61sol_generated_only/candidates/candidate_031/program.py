import pandas as pd
import numpy as np

def modify_features(X, history):
    names = [
        "f_pair_30d", "f_pair_365d", "f_pair_decay",
        "f_item_7d", "f_item_30d", "f_item_decay",
        "f_customer_7d", "f_customer_30d", "f_customer_decay",
        "f_customer_type_90d", "f_customer_colour_90d",
        "f_product_code_30d"
    ]
    out = pd.DataFrame(index=X.index)

    if history is None or len(history) == 0:
        for name in names:
            out[name] = 0.0
        return out

    h = history.reset_index(drop=True)

    def key(left, right):
        return (
            left.astype("string").fillna("<NA>") + "|" +
            right.astype("string").fillna("<NA>")
        )

    px = key(X["customer_id"], X["article_id"])
    ph = key(h["customer_id"], h["article_id"])
    cx = X["customer_id"]
    ax = X["article_id"]

    def mapped_count(candidate_key, history_key, mask=None):
        if mask is None:
            vals = history_key.value_counts()
        else:
            vals = history_key.loc[mask].value_counts()
        return candidate_key.map(vals).fillna(0).to_numpy()

    d = pd.to_numeric(h["days_ago"], errors="coerce").fillna(999999.0)

    out["f_pair_30d"] = mapped_count(px, ph, d <= 30)
    out["f_pair_365d"] = mapped_count(px, ph, d <= 365)

    decay = np.exp(-d / 30.0)
    pair_decay = decay.groupby(ph).sum()
    out["f_pair_decay"] = px.map(pair_decay).fillna(0).to_numpy()

    out["f_item_7d"] = mapped_count(ax, h["article_id"], d <= 7)
    out["f_item_30d"] = mapped_count(ax, h["article_id"], d <= 30)

    item_decay = decay.groupby(h["article_id"]).sum()
    out["f_item_decay"] = ax.map(item_decay).fillna(0).to_numpy()

    out["f_customer_7d"] = mapped_count(cx, h["customer_id"], d <= 7)
    out["f_customer_30d"] = mapped_count(cx, h["customer_id"], d <= 30)

    customer_decay = decay.groupby(h["customer_id"]).sum()
    out["f_customer_decay"] = cx.map(customer_decay).fillna(0).to_numpy()

    recent = d <= 90
    type_h = key(h["customer_id"], h["product_type_no"])
    type_x = key(cx, X["raw_i_product_type_no"])
    out["f_customer_type_90d"] = mapped_count(type_x, type_h, recent)

    colour_h = key(h["customer_id"], h["colour_group_code"])
    colour_x = key(cx, X["raw_i_colour_group_code"])
    out["f_customer_colour_90d"] = mapped_count(colour_x, colour_h, recent)

    out["f_product_code_30d"] = mapped_count(
        X["raw_i_product_code"], h["product_code"], d <= 30
    )

    return out.astype(float)
