def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Filter history within a 7-day window
    history_7day = history[history['days_ago'] <= 7]
    
    # Create new features by calculating article-specific aggregates
    F['f_article_mean_price'] = history_7day.groupby('article_id')['price'].mean()
    F['f_article_mean_product_code'] = history_7day.groupby('article_id')['product_code'].mean()
    F['f_article_mean_product_type'] = history_7day.groupby('article_id')['product_type_no'].mean()
    F['f_article_mean_graphical_appearance'] = history_7day.groupby('article_id')['graphical_appearance_no'].mean()
    F['f_article_mean_colour_group'] = history_7day.groupby('article_id')['colour_group_code'].mean()
    F['f_article_mean_perceived_colour_value'] = history_7day.groupby('article_id')['perceived_colour_value_id'].mean()
    F['f_article_mean_perceived_colour_master'] = history_7day.groupby('article_id')['perceived_colour_master_id'].mean()
    F['f_article_mean_department'] = history_7day.groupby('article_id')['department_no'].mean()
    F['f_article_mean_index_group'] = history_7day.groupby('article_id')['index_group_no'].mean()
    F['f_article_mean_section'] = history_7day.groupby('article_id')['section_no'].mean()
    F['f_article_mean_garment_group'] = history_7day.groupby('article_id')['garment_group_no'].mean()
    
    # Calculate customer-specific aggregates over article history
    F['f_customer_mean_days_ago'] = history_7day.groupby('customer_id')['days_ago'].mean()
    F['f_customer_mean_article_count'] = history_7day.groupby('customer_id')['article_id'].count()
    
    return F
