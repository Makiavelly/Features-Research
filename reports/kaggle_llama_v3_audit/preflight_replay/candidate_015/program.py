def modify_features(X, history):
    """
    Generate new features from customer and article data to enhance the recommendation model.
    
    Parameters:
    X (DataFrame): DataFrame containing candidate pairs.
    history (DataFrame): DataFrame containing past transactions.
    
    Returns:
    DataFrame: DataFrame with new features and the same 15 raw static features.
    """
    
    # Calculate number of purchases within the last 180 days and overall purchases
    history = history.groupby("customer_id").size().reset_index(name="total_purchases")
    history = history.merge(
        history.groupby("customer_id")["days_ago"]
       .apply(lambda x: (x <= 180).sum())
       .reset_index(name="recent_purchases"),
        on="customer_id",
    )
    
    # Calculate average purchase price and total purchase amount
    history = history.merge(
        history.groupby("customer_id")["price"].mean().reset_index(name="avg_purchase_price"),
        on="customer_id",
    )
    history = history.merge(
        history.groupby("customer_id")["price"].sum().reset_index(name="total_purchase_amount"),
        on="customer_id",
    )
    
    # Calculate number of different articles purchased by each customer
    history = history.merge(
        history.groupby("customer_id")["article_id"].nunique().reset_index(name="distinct_articles"),
        on="customer_id",
    )
    
    # Merge history with X to create new features
    X = X.merge(history[["customer_id", "total_purchases", "recent_purchases", "avg_purchase_price", "total_purchase_amount", "distinct_articles"]], on="customer_id", how="left")
    
    # Calculate number of purchases of the same article
    X = X.merge(
        history.groupby(["customer_id", "article_id"])["days_ago"].count().reset_index(),
        on=["customer_id", "article_id"],
        rename_columns={"days_ago": "same_article_purchases"},
        suffix="_x",
    )
    
    # Calculate average purchase price of the same article
    X = X.merge(
        history.groupby(["customer_id", "article_id"])["price"].mean().reset_index(),
        on=["customer_id", "article_id"],
        rename_columns={"price": "same_article_avg_price"},
        suffix="_x",
    )
    
    # Calculate number of purchases by category
    category_purchases = history.merge(
        history.groupby(["customer_id", "raw_i_product_type_no"])["price"].sum().reset_index(),
        on=["customer_id", "raw_i_product_type_no"],
        rename_columns={"price": "category_purchases"},
    )
    X = X.merge(
        category_purchases[["customer_id", "raw_i_product_type_no", "category_purchases"]],
        on=["customer_id", "raw_i_product_type_no"],
        how="left",
    )
    
    # Calculate average purchase price by category
    category_avg_price = history.merge(
        history.groupby(["customer_id", "raw_i_product_type_no"])["price"].mean().reset_index(),
        on=["customer_id", "raw_i_product_type_no"],
        rename_columns={"price": "category_avg_price"},
    )
    X = X.merge(
        category_avg_price[["customer_id", "raw_i_product_type_no", "category_avg_price"]],
        on=["customer_id", "raw_i_product_type_no"],
        how="left",
    )
    
    # Calculate number of purchases of articles in the same section
    X = X.merge(
        history.groupby(["customer_id", "raw_i_section_no"])["days_ago"].count().reset_index(),
        on=["customer_id", "raw_i_section_no"],
        rename_columns={"days_ago": "same_section_purchases"},
        suffix="_x",
    )
    
    # Calculate average purchase price of articles in the same section
    X = X.merge(
        history.groupby(["customer_id", "raw_i_section_no"])["price"].mean().reset_index(),
        on=["customer_id", "raw_i_section_no"],
        rename_columns={"price": "same_section_avg_price"},
        suffix="_x",
    )
    
    # Calculate number of purchases of articles with similar color
    X = X.merge(
        history.groupby(["customer_id", "raw_i_colour_group_code"])["days_ago"].count().reset_index(),
        on=["customer_id", "raw_i_colour_group_code"],
        rename_columns={"days_ago": "same_color_purchases"},
        suffix="_x",
    )
    
    # Calculate average purchase price of articles with similar color
    X = X.merge(
        history.groupby(["customer_id", "raw_i_colour_group_code"])["price"].mean().reset_index(),
        on=["customer_id", "raw_i_colour_group_code"],
        rename_columns={"price": "same_color_avg_price"},
        suffix="_x",
    )
    
    # Add new features
    X["f_total_purchases"] = X["total_purchases_x"]
    X["f_recent_purchases"] = X["recent_purchases"]
    X["f_avg_purchase_price"] = X["avg_purchase_price_x"]
    X["f_total_purchase_amount"] = X["total_purchase_amount"]
    X["f_distinct_articles"] = X["distinct_articles"]
    X["f_same_article_purchases"] = X["same_article_purchases_x"]
    X["f_same_article_avg_price"] = X["same_article_avg_price_x"]
    X["f_category_purchases"] = X["category_purchases_x"]
    X["f_category_avg_price"] = X["category_avg_price_x"]
    X["f_same_section_purchases"] = X["same_section_purchases_x"]
    X["f_same_section_avg_price"] = X["same_section_avg_price_x"]
    X["f_same_color_purchases"] = X["same_color_purchases_x"]
    X["f_same_color_avg_price"] = X["same_color_avg_price_x"]
    
    # Drop unnecessary columns
    X.drop(columns=["total_purchases_x", "recent_purchases", "avg_purchase_price_x",
                    "total_purchase_amount", "distinct_articles",
                    "same_article_purchases_x", "same_article_avg_price_x",
                    "category_purchases_x", "category_avg_price_x",
                    "same_section_purchases_x", "same_section_avg_price_x",
                    "same_color_purchases_x", "same_color_avg_price_x"], inplace=True)
    
    return X
