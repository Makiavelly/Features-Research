def modify_features(X, history):
    """
    Generate useful nontrivial recommendation features using clothing/customer domain knowledge.

    Parameters:
    X (pandas.DataFrame): dataframe containing one row per candidate pair
    history (pandas.DataFrame): dataframe containing past transactions

    Returns:
    pandas.DataFrame: dataframe with exactly X.index and row order, containing up to 48 numeric columns named f_*
    """
    
    # Calculate the mean and variance of the age feature over the selected customer cohort
    f_age_mean = history.groupby("customer_id")["customer_age"].mean().reindex(X.index)
    f_age_std = history.groupby("customer_id")["customer_age"].std().reindex(X.index)
    
    # Calculate the count of distinct product codes for each customer
    customer_product_counts = history.groupby("customer_id")["product_code"].nunique()
    f_product_count = customer_product_counts.reindex(X.index)
    
    # Calculate the average purchase price for each customer
    customer_avg_price = history.groupby("customer_id")["price"].mean()
    f_avg_price = customer_avg_price.reindex(X.index)
    
    # Calculate the number of purchases in the last 30 days for each customer
    recent_purchases = history[history["days_ago"] <= 30]
    f_recent_purchases = recent_purchases.groupby("customer_id")["days_ago"].count().reindex(X.index)
    
    # Calculate the average purchase frequency for each customer
    f_avg_frequency = history.groupby("customer_id")["days_ago"].count().reindex(X.index)
    
    # Calculate the average purchase amount for each customer
    f_avg_amount = history.groupby("customer_id")["price"].sum().reindex(X.index)
    
    # Calculate the count of article purchases for each customer
    customer_article_counts = history.groupby("customer_id")["article_id"].nunique()
    f_article_count = customer_article_counts.reindex(X.index)
    
    # Calculate the count of distinct product types for each customer
    customer_type_counts = history.groupby("customer_id")["product_type_no"].nunique()
    f_type_count = customer_type_counts.reindex(X.index)
    
    # Calculate the average purchase price per product type for each customer
    f_price_per_type = (history.groupby("customer_id")["price"].mean() *
                       history.groupby("customer_id")["product_type_no"].mean()).reindex(X.index)
    
    # Calculate the number of purchases in the last 7 days for each customer
    recent_purchases_last_week = history[history["days_ago"] <= 7]
    f_recent_last_week = recent_purchases_last_week.groupby("customer_id")["days_ago"].count().reindex(X.index)
    
    # Calculate the count of purchases per day of the week for each customer
    f_day_of_week = history.groupby("customer_id")["days_ago"].apply(lambda x: (x % 7).value_counts(normalize=True)).reindex(X.index)
    
    # Combine the original dataframe X with the new features
    new_features = pd.concat([
        f_age_mean,
        f_age_std,
        f_product_count,
        f_avg_price,
        f_recent_purchases,
        f_avg_frequency,
        f_avg_amount,
        f_article_count,
        f_type_count,
        f_price_per_type,
        f_recent_last_week,
        f_day_of_week
    ], axis=1)
    
    return new_features
