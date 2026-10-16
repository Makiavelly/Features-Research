def modify_features(X, history):
    F = pd.DataFrame(index=X.index)
    
    # Calculate the average customer age
    avg_customer_age = history.groupby('customer_id')['customer_age'].mean().reset_index()
    avg_customer_age = avg_customer_age.set_index('customer_id')
    F['f_avg_customer_age'] = avg_customer_age.reindex(F.index).fillna(0)

    # Count the number of purchases for each customer in the last 180 days
    recent_purchases = history[(history['days_ago'] >= -180) & (history['days_ago'] <= 0)]
    recent_purchases = recent_purchases.groupby('customer_id')['article_id'].count().reset_index()
    recent_purchases = recent_purchases.rename(columns={'article_id': 'f_recent_purchases'})
    recent_purchases = recent_purchases.set_index('customer_id')
    F['f_recent_purchases'] = recent_purchases.reindex(F.index).fillna(0)

    # Count the number of different product codes purchased by each customer in the last 30 days
    recent_categories = recent_purchases.groupby('customer_id')['product_code'].nunique().reset_index()
    recent_categories = recent_categories.rename(columns={'product_code': 'f_recent_categories'})
    recent_categories = recent_categories.set_index('customer_id')
    F['f_recent_categories'] = recent_categories.reindex(F.index).fillna(0)

    # Count the number of purchases for each customer in the last 30 days
    purchase_count = recent_purchases.groupby('customer_id')['customer_id'].count().reset_index()
    purchase_count = purchase_count.rename(columns={'customer_id': 'f_purchase_count'})
    purchase_count = purchase_count.set_index('customer_id')
    F['f_purchase_count'] = purchase_count.reindex(F.index).fillna(0)

    # Get the average price of purchases made by the customer in the last 30 days
    recent_purchases['price'] = recent_purchases['price'].fillna(0)
    avg_recent_price = recent_purchases.groupby('customer_id')['price'].mean().reset_index()
    avg_recent_price = avg_recent_price.rename(columns={'price': 'f_avg_recent_price'})
    avg_recent_price = avg_recent_price.set_index('customer_id')
    F['f_avg_recent_price'] = avg_recent_price.reindex(F.index).fillna(0)

    return F
