def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    # Compute mean of past purchase price
    f_mean_price = history.groupby('customer_id')['price'].mean().reindex(X['customer_id']).fillna(0).values
    
    # Compute number of past purchases within 100 days
    f_past_purchases = history[(history['days_ago'] <= 100) & (history['customer_id'].isin(X['customer_id']))].groupby('customer_id')['customer_id'].count().reindex(X['customer_id']).fillna(0).values
    
    # Compute mean of past purchases' product Types
    f_mean_product_type = history.groupby('customer_id')['product_type_no'].mean().reindex(X['customer_id']).fillna(0).values
    
    # Compute count of past purchases' colors
    f_past_colors = history.groupby('customer_id')['colour_group_code'].nunique().reindex(X['customer_id']).fillna(0).values
    
    # Compute count of article categories
    f_article_categories = history.groupby('customer_id')['article_id'].nunique().reindex(X['customer_id']).fillna(0).values
    
    # Compute average customer age
    f_avg_age = history.groupby('customer_id')['customer_age'].mean().reindex(X['customer_id']).fillna(0).values
    
    # Compute count of article categories within 100 days
    f_article_categories_100days = history[(history['days_ago'] <= 100) & (history['customer_id'].isin(X['customer_id']))].groupby('customer_id')['article_id'].nunique().reindex(X['customer_id']).fillna(0).values
    
    F['f_mean_price'] = f_mean_price
    F['f_past_purchases'] = f_past_purchases
    F['f_mean_product_type'] = f_mean_product_type
    F['f_past_colors'] = f_past_colors
    F['f_article_categories'] = f_article_categories
    F['f_avg_age'] = f_avg_age
    F['f_article_categories_100days'] = f_article_categories_100days
    
    return F
