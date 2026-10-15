def modify_features(X, history):
    """
    Generate recommendation features using clothing/customer domain knowledge.

    This function takes in a DataFrame X with candidate pairs and a history DataFrame
    containing past transactions. It returns a new DataFrame with additional features.

    The goal is to maximize validation MAP@12 on 256 validation users.

    Hypothesis:
    By incorporating customer age, fashion news frequency, product type, graphical appearance,
    colour, department, index, section, and garment group, we can improve the accuracy of
    recommended articles.

    Parameters:
    X (pd.DataFrame): Candidate pairs with customer_id and article_id.
    history (pd.DataFrame): Past transactions with customer_id, article_id, price, and days_ago.

    Returns:
    pd.DataFrame: New features with exactly X.index and row order.
    """

    # Calculate the number of days between current date and cutoff date
    # This is used to filter transactions within the last 7 days
    cutoff_days = 7

    # Filter transactions within the last 7 days
    recent_transactions = history[history['days_ago'] <= cutoff_days]

    # Calculate the number of past purchases for each customer
    # This is used to calculate the customer's purchase frequency
    customers_with_purchases = recent_transactions.groupby('customer_id')['article_id'].nunique().reset_index()
    customers_with_purchases.columns = ['customer_id', 'past_purchases']

    # Merge the customers_with_purchases DataFrame with X
    X = pd.merge(X, customers_with_purchases, on='customer_id', how='left')

    # Calculate the purchase frequency for each customer
    X['purchase_frequency'] = X['past_purchases'] / cutoff_days

    # Calculate the average price of past purchases for each customer
    recent_transactions['average_price'] = recent_transactions['price'].groupby(recent_transactions['customer_id']).mean()

    # Merge the average_price series with X
    X = pd.merge(X, recent_transactions[['customer_id', 'average_price']].groupby('customer_id')['average_price'].mean().reset_index(), on='customer_id', how='left')

    # Calculate the average price of past purchases for each customer and article
    article_average_prices = recent_transactions[['customer_id', 'article_id', 'average_price']].groupby(['customer_id', 'article_id']).mean().reset_index()

    # Merge the article_average_prices DataFrame with X
    X = pd.merge(X, article_average_prices, on=['customer_id', 'article_id'], how='left')

    # Calculate the product type similarity between each customer and article
    product_type_similarity = history[['customer_id', 'article_id', 'product_type_no']].groupby(['customer_id', 'article_id'])['product_type_no'].apply(lambda x: len(set(x))).reset_index()
    product_type_similarity.columns = ['customer_id', 'article_id', 'product_type_similarity']

    # Merge the product_type_similarity DataFrame with X
    X = pd.merge(X, product_type_similarity, on=['customer_id', 'article_id'], how='left')

    # Calculate the graphical appearance similarity between each customer and article
    graphical_appearance_similarity = history[['customer_id', 'article_id', 'graphical_appearance_no']].groupby(['customer_id', 'article_id'])['graphical_appearance_no'].apply(lambda x: len(set(x))).reset_index()
    graphical_appearance_similarity.columns = ['customer_id', 'article_id', 'graphical_appearance_similarity']

    # Merge the graphical_appearance_similarity DataFrame with X
    X = pd.merge(X, graphical_appearance_similarity, on=['customer_id', 'article_id'], how='left')

    # Calculate the colour similarity between each customer and article
    colour_similarity = history[['customer_id', 'article_id', 'colour_group_code']].groupby(['customer_id', 'article_id'])['colour_group_code'].apply(lambda x: len(set(x))).reset_index()
    colour_similarity.columns = ['customer_id', 'article_id', 'colour_similarity']

    # Merge the colour_similarity DataFrame with X
    X = pd.merge(X, colour_similarity, on=['customer_id', 'article_id'], how='left')

    # Calculate the department similarity between each customer and article
    department_similarity = history[['customer_id', 'article_id', 'department_no']].groupby(['customer_id', 'article_id'])['department_no'].apply(lambda x: len(set(x))).reset_index()
    department_similarity.columns = ['customer_id', 'article_id', 'department_similarity']

    # Merge the department_similarity DataFrame with X
    X = pd.merge(X, department_similarity, on=['customer_id', 'article_id'], how='left')

    # Calculate the index similarity between each customer and article
    index_similarity = history[['customer_id', 'article_id', 'index_group_no']].groupby(['customer_id', 'article_id'])['index_group_no'].apply(lambda x: len(set(x))).reset_index()
    index_similarity.columns = ['customer_id', 'article_id', 'index_similarity']

    # Merge the index_similarity DataFrame with X
    X = pd.merge(X, index_similarity, on=['customer_id', 'article_id'], how='left')

    # Calculate the section similarity between each customer and article
    section_similarity = history[['customer_id', 'article_id','section_no']].groupby(['customer_id', 'article_id'])['section_no'].apply(lambda x: len(set(x))).reset_index()
    section_similarity.columns = ['customer_id', 'article_id','section_similarity']

    # Merge the section_similarity DataFrame with X
    X = pd.merge(X, section_similarity, on=['customer_id', 'article_id'], how='left')

    # Calculate the garment group similarity between each customer and article
    garment_group_similarity = history[['customer_id', 'article_id', 'garment_group_no']].groupby(['customer_id', 'article_id'])['garment_group_no'].apply(lambda x: len(set(x))).reset_index()
    garment_group_similarity.columns = ['customer_id', 'article_id', 'garment_group_similarity']

    # Merge the garment_group_similarity DataFrame with X
    X = pd.merge(X, garment_group_similarity, on=['customer_id', 'article_id'], how='left')

    # Calculate the Jaccard similarity between each customer and article
    jaccard_similarity = history[['customer_id', 'article_id', 'product_code']].groupby(['customer_id', 'article_id'])['product_code'].apply(lambda x: len(set(x)) / len(x)).reset_index()
    jaccard_similarity.columns = ['customer_id', 'article_id', 'jaccard_similarity']

    # Merge the jaccard_similarity DataFrame with X
    X = pd.merge(X, jaccard_similarity, on=['customer_id', 'article_id'], how='left')

    # Calculate the average price of past purchases for each customer and article
    article_average_prices = recent_transactions[['customer_id', 'article_id', 'average_price']].groupby(['customer_id', 'article_id']).mean().reset_index()

    # Merge the article_average_prices DataFrame with X
    X = pd.merge(X, article_average_prices, on=['customer_id', 'article_id'], how='left')

    # Calculate the purchase frequency for each customer and article
    article_purchase_frequency = recent_transactions[['customer_id', 'article_id', 'past_purchases']].groupby(['customer_id', 'article_id']).mean().reset_index()

    # Merge the article_purchase_frequency DataFrame with X
    X = pd.merge(X, article_purchase_frequency, on=['customer_id', 'article_id'], how='left')

    # Calculate the product type similarity between each customer and article
    product_type_similarity = history[['customer_id', 'article_id', 'product_type_no']].groupby(['customer_id', 'article_id'])['product_type_no'].apply(lambda x: len(set(x))).reset_index()
    product_type_similarity.columns = ['customer_id', 'article_id', 'product_type_similarity']

    # Merge the product_type_similarity DataFrame with X
    X = pd.merge(X, product_type_similarity, on=['customer_id', 'article_id'], how='left')

    # Select the relevant features
    features = ['purchase_frequency', 'average_price', 'jaccard_similarity', 'product_type_similarity', 'graphical_appearance_similarity', 'colour_similarity', 'department_similarity', 'index_similarity','section_similarity', 'garment_group_similarity']

    # Return the DataFrame with the new features
    return X[features]
