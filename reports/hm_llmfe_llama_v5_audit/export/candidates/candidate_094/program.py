def modify_features(X, history):
    F = pd.DataFrame(index=X.index)

    # Compute average purchase price for each customer in the last 180 days
    avg_price = history.loc[history['days_ago'] <= 180].groupby('customer_id')['price'].mean().reindex(X['customer_id'].unique()).fillna(0)
    F['f_avg_price'] = X['customer_id'].map(avg_price)

    # Compute average number of past purchases for each customer in the last 180 days
    past_purchases = history.loc[history['days_ago'] <= 180].groupby('customer_id')['days_ago'].count().reindex(X['customer_id'].unique()).fillna(0)
    F['f_past_purchases'] = X['customer_id'].map(past_purchases)

    # Compute average age of customers who made purchases in the last 180 days
    avg_age = history.loc[history['days_ago'] <= 180].groupby('customer_id')['customer_age'].mean().reindex(X['customer_id'].unique()).fillna(0)
    F['f_avg_age'] = X['customer_id'].map(avg_age)

    # Compute average purchase price per product category for each customer in the last 180 days
    avg_price_product_category = history.loc[history['days_ago'] <= 180].groupby('customer_id')['price'].mean().reset_index()
    avg_price_product_category = avg_price_product_category.set_index('customer_id')['price'].to_frame('price')
    avg_price_product_category = avg_price_product_category.join(history[['product_code', 'price']])
    avg_price_product_category = avg_price_product_category.groupby('product_code')['price'].mean().to_frame('avg_price')
    avg_price_product_category = avg_price_product_category.rename(columns={'product_code': 'product_category', 'avg_price': 'avg_price_product_category'})

    # Merge the product categories with the main dataframe
    F = F.merge(avg_price_product_category, on='customer_id', validate='many_to_one', how='left')[['f_avg_price', 'f_past_purchases', 'f_avg_age', 'f_avg_price_product_category']]

    return F
