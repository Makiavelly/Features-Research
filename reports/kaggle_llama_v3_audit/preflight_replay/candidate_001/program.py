def modify_features(X, history):
    """
    Generate new features for customer-article pairs based on historical transactions.

    Hypothesis: Incorporating customer and article properties, along with customer-article interactions,
    will capture meaningful patterns in purchasing behavior, which can be used to improve recommendation quality.

    Features generated:
    - customer-article co-purchase frequency
    - average price of co-purchased articles
    - average days since last co-purchase
    - customer's average age when co-purchasing
    - article's average age when co-purchased
    - customer-article co-occurrence count
    - customer-article co-purchase frequency within a time window
    - customer's average purchase frequency within a time window
    - article's average purchase frequency within a time window
    - customer-article similarity based on graphical appearance
    - customer-article similarity based on color
    """

    # Ensure history has the required columns
    history = history[history.columns]

    # Generate new features
    X['f_customer_article_co_purchase_frequency'] = (
        history.groupby(['customer_id', 'article_id'])['price'].count().
        reset_index(name='customer_article_co_purchase_frequency', drop=False).
        merge(X, on=['customer_id', 'article_id'], how='left')['customer_article_co_purchase_frequency']
    )

    X['f_average_price_of_co_purchased_articles'] = (
        history.groupby(['customer_id', 'article_id'])['price'].mean().
        reset_index(name='average_price_of_co_purchased_articles', drop=False).
        merge(X, on=['customer_id', 'article_id'], how='left')['average_price_of_co_purchased_articles']
    )

    X['f_average_days_since_last_co_purchase'] = (
        history.groupby(['customer_id', 'article_id'])['days_ago'].mean().
        reset_index(name='average_days_since_last_co_purchase', drop=False).
        merge(X, on=['customer_id', 'article_id'], how='left')['average_days_since_last_co_purchase']
    )

    X['f_customer_average_age_when_co_purchasing'] = (
        history.merge(X, on=['customer_id'], how='left').
        groupby(['customer_id', 'article_id'])['raw_u_age'].mean().
        reset_index(name='customer_average_age_when_co_purchasing', drop=False).
        merge(X, on=['customer_id', 'article_id'], how='left')['customer_average_age_when_co_purchasing']
    )

    X['f_article_average_age_when_co_purchased'] = (
        history.merge(X, on=['article_id'], how='left').
        groupby(['customer_id', 'article_id'])['raw_u_age'].mean().
        reset_index(name='article_average_age_when_co_purchased', drop=False).
        merge(X, on=['customer_id', 'article_id'], how='left')['article_average_age_when_co_purchased']
    )

    X['f_customer_article_co_occurrence_count'] = (
        history.groupby(['customer_id', 'article_id']).size().
        reset_index(name='customer_article_co_occurrence_count', drop=False).
        merge(X, on=['customer_id', 'article_id'], how='left')['customer_article_co_occurrence_count']
    )

    X['f_customer_article_co_purchase_frequency_within_time_window'] = (
        history[(history['days_ago'] <= 7) & (history['days_ago'] >= 0)].
        groupby(['customer_id', 'article_id'])['price'].count().
        reset_index(name='customer_article_co_purchase_frequency_within_time_window', drop=False).
        merge(X, on=['customer_id', 'article_id'], how='left')['customer_article_co_purchase_frequency_within_time_window']
    )

    X['f_customer_average_purchase_frequency_within_time_window'] = (
        history[(history['days_ago'] <= 7) & (history['days_ago'] >= 0)].
        groupby(['customer_id'])['price'].count().
        reset_index(name='customer_average_purchase_frequency_within_time_window', drop=False).
        merge(X, on=['customer_id'], how='left')['customer_average_purchase_frequency_within_time_window']
    )

    X['f_article_average_purchase_frequency_within_time_window'] = (
        history[(history['days_ago'] <= 7) & (history['days_ago'] >= 0)].
        groupby(['article_id'])['price'].count().
        reset_index(name='article_average_purchase_frequency_within_time_window', drop=False).
        merge(X, on=['article_id'], how='left')['article_average_purchase_frequency_within_time_window']
    )

    X['f_customer_article_similarity_graphical_appearance'] = (
        history.groupby(['customer_id', 'article_id'])['raw_i_graphical_appearance_no'].mean().
        reset_index(name='customer_article_similarity_graphical_appearance', drop=False).
        merge(X, on=['customer_id', 'article_id'], how='left')['customer_article_similarity_graphical_appearance']
    )

    X['f_customer_article_similarity_color'] = (
        history.groupby(['customer_id', 'article_id'])['raw_i_colour_group_code'].mean().
        reset_index(name='customer_article_similarity_color', drop=False).
        merge(X, on=['customer_id', 'article_id'], how='left')['customer_article_similarity_color']
    )

    return X
