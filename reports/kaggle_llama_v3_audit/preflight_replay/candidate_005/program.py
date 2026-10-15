def modify_features(X, history):
    """
    Generate new features based on past transactions and user information.

    Hypothesis: Users with similar past purchases and demographic characteristics have a higher probability of purchasing similar articles in the future.
    """

    # Merge customer purchase history with the candidate pairs dataframe
    merged = pd.merge(X, history, on=['customer_id', 'article_id'], how='left', suffixes=('', '_history'))

    # Calculate the average price of past purchases by customer
    merged['avg_price_history'] = merged.groupby('customer_id')['price_history'].transform('mean')

    # Calculate the number of past purchases by customer
    merged['num_purchases_history'] = merged.groupby('customer_id')['article_id_history'].transform('count')

    # Calculate the average price of past purchases by article
    merged['avg_price_article_history'] = merged.groupby('article_id')['price_history'].transform('mean')

    # Calculate the number of past purchases by article
    merged['num_purchases_article_history'] = merged.groupby('article_id')['article_id_history'].transform('count')

    # Calculate the average age of customers who purchased each article
    merged['avg_age_article_history'] = merged.groupby('article_id')['raw_u_age'].transform('mean')

    # Calculate the proportion of customers who purchased each article and have a membership status
    merged['prop_member_article_history'] = merged.groupby('article_id')['raw_u_club_member_status'].transform('mean')

    # Calculate the proportion of customers who purchased each article and received fashion news
    merged['prop_news_article_history'] = merged.groupby('article_id')['raw_u_fashion_news_frequency'].transform('mean')

    # Calculate the average price of past purchases by customer and article category
    merged['avg_price_category_history'] = merged.groupby(['customer_id', 'raw_i_product_type_no'])['price_history'].transform('mean')

    # Calculate the number of past purchases by customer and article category
    merged['num_purchases_category_history'] = merged.groupby(['customer_id', 'raw_i_product_type_no'])['article_id_history'].transform('count')

    # Filter out columns that have been merged or renamed
    merged_features = merged[['customer_id', 'article_id', 'raw_u_age', 'raw_u_fn', 'raw_u_active', 'raw_u_club_member_status',
                              'raw_u_fashion_news_frequency', 'raw_i_product_code', 'raw_i_product_type_no', 'raw_i_graphical_appearance_no',
                              'raw_i_colour_group_code', 'raw_i_perceived_colour_value_id', 'raw_i_perceived_colour_master_id',
                              'raw_i_department_no', 'raw_i_index_group_no', 'raw_i_section_no', 'raw_i_garment_group_no',
                              'price','sales_channel_id', 'days_ago', 'avg_price_history', 'num_purchases_history',
                              'avg_price_article_history', 'num_purchases_article_history',
                              'avg_age_article_history', 'prop_member_article_history', 'prop_news_article_history',
                              'avg_price_category_history', 'num_purchases_category_history']]

    return merged_features
