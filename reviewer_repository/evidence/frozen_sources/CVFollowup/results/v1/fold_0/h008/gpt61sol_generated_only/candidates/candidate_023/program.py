import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history
    c = X["customer_id"]
    a = X["article_id"]

    def item_count(z):
        return a.map(z.groupby("article_id").size()).fillna(0)

    def user_count(z):
        return c.map(z.groupby("customer_id").size()).fillna(0)

    def pair_value(z, column=None, operation="size"):
        if z.empty:
            return pd.Series(0.0, index=X.index)
        g = z.groupby(["customer_id", "article_id"])
        if column is None:
            q = g.size()
        elif operation == "min":
            q = g[column].min()
        elif operation == "mean":
            q = g[column].mean()
        elif operation == "sum":
            q = g[column].sum()
        else:
            q = g[column].max()
        key = pd.MultiIndex.from_arrays([
            c.to_numpy(), a.to_numpy()
        ])
        return pd.Series(q.reindex(key).to_numpy(), index=X.index).fillna(0)

    def category_count(z, raw_col, hist_col):
        if z.empty:
            return pd.Series(0.0, index=X.index)
        sentinel = -999999999
        zz = z.assign(_category=z[hist_col].fillna(sentinel))
        q = zz.groupby(["customer_id", "_category"]).size()
        key = pd.MultiIndex.from_arrays([
            c.to_numpy(), X[raw_col].fillna(sentinel).to_numpy()
        ])
        return pd.Series(q.reindex(key).to_numpy(), index=X.index).fillna(0)

    h7 = h.loc[h["days_ago"] <= 7]
    h30 = h.loc[h["days_ago"] <= 30]
    h90 = h.loc[h["days_ago"] <= 90]

    out["f_item_pop_7d"] = item_count(h7)
    out["f_item_pop_30d"] = item_count(h30)
    out["f_item_pop_90d"] = item_count(h90)
    out["f_item_pop_all"] = item_count(h)
    out["f_item_velocity"] = out["f_item_pop_7d"] / (
        out["f_item_pop_30d"] + 1.0
    )
    out["f_item_recency"] = a.map(
        h.groupby("article_id")["days_ago"].min()
    )

    out["f_user_item_7d"] = pair_value(h7)
    out["f_user_item_30d"] = pair_value(h30)
    out["f_user_item_all"] = pair_value(h)
    out["f_user_item_recency"] = pair_value(h, "days_ago", "min")
    out["f_user_item_price"] = pair_value(h, "price", "mean")

    out["f_user_purchases_7d"] = user_count(h7)
    out["f_user_purchases_30d"] = user_count(h30)
    out["f_user_purchases_90d"] = user_count(h90)
    out["f_user_purchases_all"] = user_count(h)
    out["f_user_recency"] = c.map(
        h.groupby("customer_id")["days_ago"].min()
    )

    out["f_user_type_30d"] = category_count(
        h30, "raw_i_product_type_no", "product_type_no"
    )
    out["f_user_type_all"] = category_count(
        h, "raw_i_product_type_no", "product_type_no"
    )
    out["f_user_department_30d"] = category_count(
        h30, "raw_i_department_no", "department_no"
    )
    out["f_user_section_30d"] = category_count(
        h30, "raw_i_section_no", "section_no"
    )
    out["f_user_colour_90d"] = category_count(
        h90, "raw_i_colour_group_code", "colour_group_code"
    )
    out["f_user_product_30d"] = category_count(
        h30, "raw_i_product_code", "product_code"
    )
    out["f_user_garment_30d"] = category_count(
        h30, "raw_i_garment_group_no", "garment_group_no"
    )

    out["f_item_unique_buyers"] = a.map(
        h.groupby("article_id")["customer_id"].nunique()
    ).fillna(0)
    out["f_item_mean_price"] = a.map(
        h.groupby("article_id")["price"].mean()
    )
    out["f_user_mean_price"] = c.map(
        h.groupby("customer_id")["price"].mean()
    )
    out["f_user_recent_price"] = c.map(
        h30.groupby("customer_id")["price"].mean()
    )
    out["f_user_channel1_share"] = c.map(
        h.assign(_channel=(h["sales_channel_id"] == 1).astype(float))
        .groupby("customer_id")["_channel"].mean()
    )
    out["f_age"] = X["raw_u_age"]
    out["f_user_active"] = X["raw_u_active"]
    out["f_user_club"] = X["raw_u_club_member_status"]

    return out.replace([np.inf, -np.inf], np.nan)
