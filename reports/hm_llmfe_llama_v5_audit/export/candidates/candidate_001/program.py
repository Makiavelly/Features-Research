def modify_features(X, history):
    # Calculate average past purchase price
    avg_price = history.groupby('customer_id')['price'].mean().reindex(X['customer_id']).fillna(0)

    # Calculate average past purchase days ago
    avg_days_ago = history.groupby('customer_id')['days_ago'].mean().reindex(X['customer_id']).fillna(0)

    # Calculate average past purchase product type
    avg_product_type_no = history.groupby('customer_id')['product_type_no'].mean().reindex(X['customer_id']).fillna(0)

    # Calculate average past purchase department no
    avg_department_no = history.groupby('customer_id')['department_no'].mean().reindex(X['customer_id']).fillna(0)

    # Create a new DataFrame with the calculated features
    F = pd.DataFrame({
        'f_average_price': avg_price.values,
        'f_average_days_ago': avg_days_ago.values,
        'f_average_product_type_no': avg_product_type_no.values,
        'f_average_department_no': avg_department_no.values
    }, index=X.index)

    return F
