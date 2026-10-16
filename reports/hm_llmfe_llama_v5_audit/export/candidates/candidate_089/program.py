def modify_features(X, history):
    # Filter days_ago for a 7-day history window, calculate past purchases and price mean for each customer
    history_7_days = history[history['days_ago'] <= 7]
    avg_price = history_7_days.groupby('customer_id')['price'].mean().reset_index()
    past_purchases = history_7_days['customer_id'].value_counts().rename('past_purchases').to_frame()
    past_purchases['customer_id'] = past_purchases.index

    # Compute customer average age, count of each category, and most frequent article
    avg_age = history.groupby('customer_id')['customer_age'].mean().reset_index()
    count_categories = history.groupby('customer_id')['product_code'].nunique().reset_index()
    most_frequent_article = history.groupby('customer_id')['article_id'].apply(lambda x: x.value_counts().index[0]).reset_index(name='most_frequent_article')

    # Merge the computed features into one DataFrame and assign numeric columns into F
    F = pd.merge(avg_age, count_categories, on='customer_id', validate='many_to_one')
    F = pd.merge(F, past_purchases, on='customer_id', validate='many_to_one')
    F = pd.merge(F, most_frequent_article, on='customer_id', validate='many_to_one')

    # Assign values positionally to F
    F = F[['customer_id', 'avg_price', 'past_purchases', 'count_categories','most_frequent_article']]

    return F
