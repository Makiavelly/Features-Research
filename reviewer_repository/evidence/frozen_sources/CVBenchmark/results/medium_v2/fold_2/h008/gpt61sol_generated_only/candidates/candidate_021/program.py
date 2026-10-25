import numpy as np
import pandas as pd


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history

    def user_map(s):
        return X["customer_id"].map(s).fillna(0.0)

    def item_map(s):
        return X["article_id"].map(s).fillna(0.0)

    def pair_map(s, left="customer_id", right="article_id"):
        if len(s) == 0:
            return pd.Series(0.0, index=X.index)
        k = pd.MultiIndex.from_arrays(
            [X[left].to_numpy(), X[right].to_numpy()]
        )
        return pd.Series(s.reindex(k).to_numpy(), index=X.index).fillna(0.0)

    def category_map(s, raw_col):
        if len(s) == 0:
            return pd.Series(0.0, index=X.index)
        k = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X[raw_col].to_numpy()]
        )
        return pd.Series(s.reindex(k).to_numpy(), index=X.index).fillna(0.0)

    if len(h):
        for d, tag in ((7, "7d"), (30, "30d"), (90, "90d"), (365, "365d")):
            z = h.loc[h["days_ago"] <= d]
            out["f_user_purchases_" + tag] = user_map(
                z.groupby("customer_id", sort=False).size()
            )
            out["f_item_purchases_" + tag] = item_map(
                z.groupby("article_id", sort=False).size()
            )

        uc = h.groupby("customer_id", sort=False).size()
        ic = h.groupby("article_id", sort=False).size()
        out["f_user_purchases_all"] = user_map(uc)
        out["f_item_purchases_all"] = item_map(ic)

        out["f_customer_recency"] = user_map(
            h.groupby("customer_id", sort=False)["days_ago"].min()
        )
        out["f_item_recency"] = item_map(
            h.groupby("article_id", sort=False)["days_ago"].min()
        )
        out["f_pair_purchases"] = pair_map(
            h.groupby(["customer_id", "article_id"], sort=False).size()
        )
        out["f_pair_recency"] = pair_map(
            h.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min()
        )

        recent = h.loc[h["days_ago"] <= 30]
        recent_i = recent.groupby("article_id", sort=False).size()
        out["f_item_recent_share"] = item_map(recent_i) / (item_map(ic) + 1.0)
        out["f_item_unique_customers"] = item_map(
            h.groupby("article_id", sort=False)["customer_id"].nunique()
        )

        weighted = h.assign(
            _w=np.exp(-h["days_ago"].astype(float) / 21.0)
        )
        out["f_item_weighted_popularity"] = item_map(
            weighted.groupby("article_id", sort=False)["_w"].sum()
        )
        out["f_user_weighted_activity"] = user_map(
            weighted.groupby("customer_id", sort=False)["_w"].sum()
        )

        for col, raw in (
            ("product_code", "raw_i_product_code"),
            ("product_type_no", "raw_i_product_type_no"),
            ("department_no", "raw_i_department_no"),
            ("section_no", "raw_i_section_no"),
            ("colour_group_code", "raw_i_colour_group_code"),
        ):
            g = h.groupby(["customer_id", col], sort=False).size()
            out["f_user_" + col + "_purchases"] = category_map(g, raw)
            out["f_user_" + col + "_share"] = category_map(g, raw) / (
                user_map(uc) + 1.0
            )

        pmean_u = h.groupby("customer_id", sort=False)["price"].mean()
        pmean_i = h.groupby("article_id", sort=False)["price"].mean()
        out["f_user_mean_price"] = user_map(pmean_u)
        out["f_item_mean_price"] = item_map(pmean_i)
        out["f_price_ratio_to_user"] = (
            item_map(pmean_i) / (user_map(pmean_u) + 0.01)
        )
    else:
        names = [
            "f_user_purchases_7d", "f_item_purchases_7d",
            "f_user_purchases_30d", "f_item_purchases_30d",
            "f_user_purchases_90d", "f_item_purchases_90d",
            "f_user_purchases_365d", "f_item_purchases_365d",
            "f_user_purchases_all", "f_item_purchases_all",
            "f_customer_recency", "f_item_recency", "f_pair_purchases",
            "f_pair_recency", "f_item_recent_share",
            "f_item_unique_customers", "f_item_weighted_popularity",
            "f_user_weighted_activity", "f_user_mean_price",
            "f_item_mean_price", "f_price_ratio_to_user",
            "f_user_product_code_purchases", "f_user_product_code_share",
            "f_user_product_type_no_purchases", "f_user_product_type_no_share",
            "f_user_department_no_purchases", "f_user_department_no_share",
            "f_user_section_no_purchases", "f_user_section_no_share",
            "f_user_colour_group_code_purchases",
            "f_user_colour_group_code_share",
        ]
        for n in names:
            out[n] = 0.0

    out["f_static_age"] = X["raw_u_age"]
    out["f_static_active"] = X["raw_u_active"]
    out["f_static_club"] = X["raw_u_club_member_status"]
    out["f_static_product_type"] = X["raw_i_product_type_no"]
    out["f_static_department"] = X["raw_i_department_no"]
    return out.astype(float)
