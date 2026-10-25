import pandas as pd
import numpy as np

def modify_features(X, history):
    out = pd.DataFrame(index=X.index)

    def grouped_count(frame, cols):
        if len(frame) == 0:
            return pd.Series(dtype="float64")
        return frame.groupby(cols, sort=False).size().astype(float)

    def pair_feature(frame, name):
        s = grouped_count(frame, ["customer_id", "article_id"])
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        out[name] = s.reindex(keys).to_numpy()

    def customer_feature(frame, name):
        if len(frame) == 0:
            out[name] = np.nan
        else:
            s = frame.groupby("customer_id", sort=False).size().astype(float)
            out[name] = X["customer_id"].map(s).to_numpy()

    def item_feature(frame, name):
        if len(frame) == 0:
            out[name] = np.nan
        else:
            s = frame.groupby("article_id", sort=False).size().astype(float)
            out[name] = X["article_id"].map(s).to_numpy()

    pair_feature(history.loc[history["days_ago"] <= 7], "f_pair_count_7d")
    pair_feature(history.loc[history["days_ago"] <= 30], "f_pair_count_30d")
    pair_feature(history.loc[history["days_ago"] <= 180], "f_pair_count_180d")

    if len(history):
        rec = history.groupby(["customer_id", "article_id"], sort=False)["days_ago"].min()
        keys = pd.MultiIndex.from_arrays(
            [X["customer_id"].to_numpy(), X["article_id"].to_numpy()]
        )
        out["f_pair_recency"] = rec.reindex(keys).to_numpy()
        cre = history.groupby("customer_id", sort=False)["days_ago"].min()
        out["f_customer_recency"] = X["customer_id"].map(cre).to_numpy()
    else:
        out["f_pair_recency"] = np.nan
        out["f_customer_recency"] = np.nan

    customer_feature(
        history.loc[history["days_ago"] <= 30], "f_customer_count_30d"
    )
    customer_feature(
        history.loc[history["days_ago"] <= 180], "f_customer_count_180d"
    )
    item_feature(history.loc[history["days_ago"] <= 30], "f_item_count_30d")
    item_feature(history.loc[history["days_ago"] <= 180], "f_item_count_180d")

    recent = history.loc[history["days_ago"] <= 180]
    keys_customer = X["customer_id"].to_numpy()

    for raw_col, hist_col, feature_name in [
        ("raw_i_product_type_no", "product_type_no", "f_customer_product_type_180d"),
        ("raw_i_department_no", "department_no", "f_customer_department_180d"),
        ("raw_i_section_no", "section_no", "f_customer_section_180d"),
    ]:
        if len(recent):
            stats = recent.groupby(
                ["customer_id", hist_col], sort=False
            ).size().astype(float)
            keys = pd.MultiIndex.from_arrays(
                [keys_customer, X[raw_col].to_numpy()]
            )
            out[feature_name] = stats.reindex(keys).to_numpy()
        else:
            out[feature_name] = np.nan

    return out.astype(float)
