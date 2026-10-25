import numpy as np
import pandas as pd


def modify_features(X, history):
    out = pd.DataFrame(index=X.index)
    h = history

    def user_map(s):
        return X["customer_id"].map(s).fillna(0.0)

    def item_map(s):
        return X["article_id"].map(s).fillna(0.0)

    def pair_map(s, left, right):
        q = pd.MultiIndex.from_arrays(
            [X[left].to_numpy(), X[right].to_numpy()]
        )
        try:
            v = s.reindex(q).to_numpy()
        except Exception:
            v = pd.Series(q.map(s), index=X.index).to_numpy()
        return pd.Series(v, index=X.index).fillna(0.0)

    if len(h):
        hdays = h["days_ago"].astype(float)

        for d, tag in ((7, "7d"), (30, "30d"), (180, "180d")):
            z = h.loc[hdays <= d]
            out["f_user_count_" + tag] = user_map(
                z.groupby("customer_id", sort=False).size()
            )
            out["f_item_count_" + tag] = item_map(
                z.groupby("article_id", sort=False).size()
            )

        out["f_user_count_all"] = user_map(
            h.groupby("customer_id", sort=False).size()
        )
        out["f_item_count_all"] = item_map(
            h.groupby("article_id", sort=False).size()
        )

        p = h.groupby(["customer_id", "article_id"], sort=False)
        out["f_pair_count_all"] = pair_map(
            p.size(), "customer_id", "article_id"
        )
        out["f_pair_count_30d"] = pair_map(
            h.loc[hdays <= 30].groupby(
                ["customer_id", "article_id"], sort=False
            ).size(),
            "customer_id", "article_id",
        )
        out["f_pair_recency"] = pair_map(
            p["days_ago"].min(), "customer_id", "article_id"
        )

        out["f_customer_recency"] = user_map(
            h.groupby("customer_id", sort=False)["days_ago"].min()
        )
        out["f_item_recency"] = item_map(
            h.groupby("article_id", sort=False)["days_ago"].min()
        )
        out["f_item_unique_users"] = item_map(
            h.groupby("article_id", sort=False)["customer_id"].nunique()
        )

        weighted = h.assign(
            _w=np.exp(-hdays / 21.0),
            _w7=np.exp(-hdays / 7.0)
        )
        out["f_item_weighted_demand"] = item_map(
            weighted.groupby("article_id", sort=False)["_w"].sum()
        )
        out["f_user_weighted_demand"] = user_map(
            weighted.groupby("customer_id", sort=False)["_w"].sum()
        )

        for col, raw, name in (
            ("product_code", "raw_i_product_code", "product"),
            ("product_type_no", "raw_i_product_type_no", "type"),
            ("department_no", "raw_i_department_no", "department"),
            ("colour_group_code", "raw_i_colour_group_code", "colour"),
            ("section_no", "raw_i_section_no", "section"),
        ):
            out["f_user_" + name + "_count"] = pair_map(
                h.groupby(["customer_id", col], sort=False).size(),
                "customer_id", raw
            )
            out["f_user_" + name + "_weighted"] = pair_map(
                weighted.groupby(["customer_id", col], sort=False)["_w7"].sum(),
                "customer_id", raw
            )

        out["f_item_price_mean"] = item_map(
            h.groupby("article_id", sort=False)["price"].mean()
        )
        out["f_user_price_mean"] = user_map(
            h.groupby("customer_id", sort=False)["price"].mean()
        )
        out["f_item_channel2_share"] = item_map(
            h.assign(_c2=(h["sales_channel_id"] == 2).astype(float))
             .groupby("article_id", sort=False)["_c2"].mean()
        )
    else:
        names = [
            "f_user_count_7d", "f_item_count_7d",
            "f_user_count_30d", "f_item_count_30d",
            "f_user_count_180d", "f_item_count_180d",
            "f_user_count_all", "f_item_count_all",
            "f_pair_count_all", "f_pair_count_30d", "f_pair_recency",
            "f_customer_recency", "f_item_recency", "f_item_unique_users",
            "f_item_weighted_demand", "f_user_weighted_demand",
            "f_user_product_count", "f_user_product_weighted",
            "f_user_type_count", "f_user_type_weighted",
            "f_user_department_count", "f_user_department_weighted",
            "f_user_colour_count", "f_user_colour_weighted",
            "f_user_section_count", "f_user_section_weighted",
            "f_item_price_mean", "f_user_price_mean",
            "f_item_channel2_share",
        ]
        for name in names:
            out[name] = 0.0

    out["f_static_age"] = X["raw_u_age"]
    out["f_static_active"] = X["raw_u_active"]
    out["f_static_club"] = X["raw_u_club_member_status"]
    out["f_static_product_type"] = X["raw_i_product_type_no"]
    out["f_static_department"] = X["raw_i_department_no"]
    out["f_static_section"] = X["raw_i_section_no"]
    out["f_static_colour"] = X["raw_i_colour_group_code"]
    return out.astype(float)
