def modify_features(X, history):
    """
    Hypothesis: The ranking of candidate articles per customer is influenced by the customer's age, fashion news frequency, 
    product type, graphical appearance, and past purchases in the same department. The overall hypothesis is that a customer 
    is more likely to purchase an article if they have previously purchased similar articles in the same department.

    Returns:
        A DataFrame with new features, where each row corresponds to a candidate pair and each column represents a new feature.
    """
    
    # Get the customer ID, article ID, and days ago from X and history
    X_customer_id = X["customer_id"]
    X_article_id = X["article_id"]
    X_days_ago = X["days_ago"]
    
    hist_customer_id = history["customer_id"]
    hist_article_id = history["article_id"]
    hist_days_ago = history["days_ago"]
    
    # Calculate the average age of customers who purchased articles in the same department as the current candidate pair
    avg_age = pd.merge(hist_customer_id, X_customer_id, left_on="customer_id", right_on="customer_id", how="outer")["customer_id"].map(lambda x: history[history["customer_id"] == x]["raw_u_age"].mean())  
    X["f_avg_age_in_dept"] = X["customer_id"].map(lambda x: avg_age[x] if x in avg_age else np.nan)
    
    # Count the number of articles purchased by customers in the same department as the current candidate pair
    num_purchases = pd.merge(hist_customer_id, X_customer_id, left_on="customer_id", right_on="customer_id", how="outer")["customer_id"].map(lambda x: history[history["customer_id"] == x]["customer_id"].value_counts().max())  
    X["f_num_purchases_in_dept"] = X["customer_id"].map(lambda x: num_purchases[x] if x in num_purchases else 0)
    
    # Calculate the average price of articles purchased by customers in the same department as the current candidate pair
    avg_price = pd.merge(hist_customer_id, X_customer_id, left_on="customer_id", right_on="customer_id", how="outer")["customer_id"].map(lambda x: history[history["customer_id"] == x]["price"].mean())  
    X["f_avg_price_in_dept"] = X["customer_id"].map(lambda x: avg_price[x] if x in avg_price else np.nan)
    
    # Count the number of different product types purchased by customers in the same department as the current candidate pair
    num_product_types = pd.merge(hist_customer_id, X_customer_id, left_on="customer_id", right_on="customer_id", how="outer")["customer_id"].map(lambda x: history[history["customer_id"] == x]["raw_i_product_type_no"].nunique())  
    X["f_num_product_types_in_dept"] = X["customer_id"].map(lambda x: num_product_types[x] if x in num_product_types else 0)
    
    # Calculate the average fashion news frequency of customers who purchased articles in the same department as the current candidate pair
    avg_fashion_news_freq = pd.merge(hist_customer_id, X_customer_id, left_on="customer_id", right_on="customer_id", how="outer")["customer_id"].map(lambda x: history[history["customer_id"] == x]["raw_u_fashion_news_frequency"].mean())  
    X["f_avg_fashion_news_freq_in_dept"] = X["customer_id"].map(lambda x: avg_fashion_news_freq[x] if x in avg_fashion_news_freq else np.nan)
    
    # Count the number of articles purchased by customers in the same department as the current candidate pair with the same graphical appearance
    num_same_appearances = pd.merge(hist_customer_id, X_customer_id, left_on="customer_id", right_on="customer_id", how="outer")["customer_id"].map(lambda x: history[history["customer_id"] == x][("raw_i_graphical_appearance_no", "raw_i_product_code")].apply(lambda row: ((row["raw_i_graphical_appearance_no"] == row["raw_i_graphical_appearance_no"]) & (row["raw_i_product_code"] == row["raw_i_product_code"]))).sum())  
    X["f_num_same_appearances_in_dept"] = X["customer_id"].map(lambda x: num_same_appearances[x] if x in num_same_appearances else 0)
    
    return X
