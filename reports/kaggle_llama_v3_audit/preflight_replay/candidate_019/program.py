def modify_features(X, history):
    """
    Generate new features for the clothing recommendation problem.

    This function takes in a DataFrame X containing candidate pairs and a DataFrame history
    containing past transactions. It generates new features based on customer and article
    attributes, as well as their interactions. The function returns a DataFrame with the same
    index as X and additional numeric columns named f_*. The host always appends the same 15
    raw static features.

    Hypothesis: By capturing the customer-article interactions and dynamics in the sales history,
    we can identify useful patterns that inform article recommendations.

    Parameters:
    X (DataFrame): Candidate pairs with one row per pair.
    history (DataFrame): Past transactions with customer and article attributes.

    Returns:
    DataFrame: X with additional numeric columns named f_*
    """

    # New features: vectorized groupby/merge/map
    # Generate frequency of each article type per customer
    X['f_article_type_freq'] = history.groupby(['customer_id'])['raw_i_product_type_no'].transform('mean')
    # Generate frequency of each clothing color per customer
    X['f_clothing_color_freq'] = history.groupby(['customer_id'])['raw_i_colour_group_code'].transform('mean')
    # Generate frequency of each customer-buying article pair
    X['f_customer_item_freq'] = history.groupby(['customer_id', 'article_id'])['price'].transform('count')

    # New features: time windows
    # Generate average purchase price per customer within the last 30 days
    X['frecent_price_avg'] = history[history['days_ago'] <= 30].groupby(['customer_id'])['price'].transform('mean')
    # Generate average purchase days ago per customer within the last 30 days
    X['frecent_days_avg'] = history[history['days_ago'] <= 30].groupby(['customer_id'])['days_ago'].transform('mean')

    # New features: affinity
    # Generate similarity in clothing purchases between customers
    X['f_customer_similarity'] = history.groupby('customer_id')['raw_i_product_code'].transform(lambda x: x.diff().mean())
    # Generate similarity in article types between customers
    X['f_article_type_similarity'] = history.groupby('customer_id')['raw_i_product_type_no'].transform(lambda x: x.diff().mean())

    # New features: interactions
    # Generate interaction between customer fashion news frequency and article perceived color value id
    X['f_interaction'] = history['raw_u_fashion_news_frequency'] * history['raw_i_perceived_colour_value_id']

    return X
