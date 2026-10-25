def modify_features(X, history):
    import pandas as pd
    import numpy as np

    out = pd.DataFrame(index=X.index)
    h = history
    u = X["customer_id"].to_numpy()
    a = X["article_id"].to_numpy()
    n = len(X)

    names = (
        "f_user_mean_price", "f_user_price_std", "f_item_mean_price",
        "f_item_price_std", "f_user_channel2_rate", "f_item_channel2_rate",
        "f_user_recent_price", "f_article_recent_buyers",
        "f_user_article_price_gap", "f_user_recent_categories",
    )
    if h is None or len(h) == 0:
        for name in names:
            out[name] = 0.0
        return out

    d = pd.to_numeric(h["days_ago"], errors="coerce")
    price = pd.to_numeric(h["price"], errors="coerce")
    z = h.assign(_price=price)
    recent = z.loc[d <= 45]

    user_mean = z.groupby("customer_id", sort=False)["_price"].mean()
    user_std = z.groupby("customer_id", sort=False)["_price"].std()
    item_mean = z.groupby("article_id", sort=False)["_price"].mean()
    item_std = z.groupby("article_id", sort=False)["_price"].std()

    out["f_user_mean_price"] = X["customer_id"].map(user_mean).to_numpy()
    out["f_user_price_std"] = X["customer_id"].map(user_std).to_numpy()
    out["f_item_mean_price"] = X["article_id"].map(item_mean).to_numpy()
    out["f_item_price_std"] = X["article_id"].map(item_std).to_numpy()

    ch_user = z.groupby("customer_id", sort=False)["sales_channel_id"].mean()
    ch_item = z.groupby("article_id", sort=False)["sales_channel_id"].mean()
    out["f_user_channel2_rate"] = X["customer_id"].map(ch_user).to_numpy() - 1.0
    out["f_item_channel2_rate"] = X["article_id"].map(ch_item).to_numpy() - 1.0

    recent_mean = recent.groupby("customer_id", sort=False)["_price"].mean()
    out["f_user_recent_price"] = X["customer_id"].map(recent_mean).to_numpy()

    buyers = recent.groupby("article_id", sort=False)["customer_id"].nunique()
    out["f_article_recent_buyers"] = X["article_id"].map(buyers).fillna(0).to_numpy()

    up = z.groupby(["customer_id", "article_id"], sort=False)["_price"].mean()
    keys = pd.MultiIndex.from_arrays([u, a])
    pair_price = up.reindex(keys).to_numpy()
    user_price = X["customer_id"].map(user_mean).to_numpy()
    out["f_user_article_price_gap"] = pair_price - user_price

    cat = recent.groupby("customer_id", sort=False)["department_no"].nunique()
    out["f_user_recent_categories"] = X["customer_id"].map(cat).fillna(0).to_numpy()

    return out.replace([np.inf, -np.inf], np.nan)
