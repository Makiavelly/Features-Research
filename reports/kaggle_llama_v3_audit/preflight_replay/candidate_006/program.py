def modify_features(X, history):
    """
    Generate novel features for customer-article pairs to inform recommendation.
    Hypothesis: Customer/article interactions and past transactions are strong predictors of future engagements.
    Returns a DataFrame with rows corresponding to X and columns f_*
    """
    
    # Calculate the average price of products purchased by each customer in the past 180 days
    avg_price = history.groupby('customer_id')['price'].apply(lambda x: x.shift(180).mean() if not x.empty else np.nan).reset_index(drop=True)
    X = X.merge(avg_price, left_on='customer_id', right_index=True, suffixes=('', '_avg_price'))

    # Count the number of times each customer purchased articles from the same product category in the past 180 days
    prod_cats = history['product_code'].groupby(history['customer_id']).apply(lambda x: x.iloc[:180].value_counts().index[0] if len(x) == 180 else np.nan).reset_index(drop=True)
    X = X.merge(prod_cats, left_on='customer_id', right_index=True, suffixes=('', '_prod_cat'))

    # Determine whether customers have purchased articles from the same department in the past 180 days
    dept_purchases = history['department_no'].groupby(history['customer_id']).apply(lambda x: x.iloc[:180].nunique() == 1 if len(x) == 180 else np.nan).reset_index(drop=True)
    X = X.merge(dept_purchases, left_on='customer_id', right_index=True, suffixes=('', '_dept_purchases'))

    # Calculate the average time between purchases for each customer in the past 180 days
    avg_time_between_purchases = history.groupby('customer_id')['days_ago'].apply(lambda x: x.iloc[:180].mean() if len(x) == 180 else np.nan).reset_index(drop=True)
    X = X.merge(avg_time_between_purchases, left_on='customer_id', right_index=True, suffixes=('', '_avg_time_between_purchases'))

    # Count the number of different sales channels used by each customer in the past 180 days
    sales_channels = history['sales_channel_id'].groupby(history['customer_id']).apply(lambda x: x.iloc[:180].nunique() if len(x) == 180 else np.nan).reset_index(drop=True)
    X = X.merge(sales_channels, left_on='customer_id', right_index=True, suffixes=('', '_sales_channels'))

    # Calculate the ratio of purchases made by each customer in the past 180 days from the same product category
    prod_cat_ratio = history['product_code'].groupby(history['customer_id']).apply(lambda x: x.iloc[:180].value_counts(normalize=True).iloc[0,0] if len(x) == 180 else np.nan).reset_index(drop=True)
    X = X.merge(prod_cat_ratio, left_on='customer_id', right_index=True, suffixes=('', '_prod_cat_ratio'))

    # Determine the average age of customers who purchased articles from each product category in the past 180 days
    avg_age = history.groupby('product_code')['customer_age'].apply(lambda x: x.iloc[:180].mean() if len(x) == 180 else np.nan).reset_index(drop=True)
    X = X.merge(avg_age, left_on='product_code', right_index=True, suffixes=('', '_avg_age'))

    # Calculate the average number of articles purchased by each customer in the past 180 days
    avg_articles_purchased = history.groupby('customer_id')['article_id'].apply(lambda x: x.iloc[:180].nunique() if len(x) == 180 else np.nan).reset_index(drop=True)
    X = X.merge(avg_articles_purchased, left_on='customer_id', right_index=True, suffixes=('', '_avg_articles_purchased'))

    # Determine the proportion of customers who purchased articles from the same department in the past 180 days
    dept_proportion = history['department_no'].groupby(history['customer_id']).apply(lambda x: (x.iloc[:180] == x.iloc[:180].iloc[0]).sum() / len(x) if len(x) == 180 else np.nan).reset_index(drop=True)
    X = X.merge(dept_proportion, left_on='customer_id', right_index=True, suffixes=('', '_dept_proportion'))

    # Calculate the average price of products purchased by each customer in the past 180 days, excluding purchases from the same product category
    avg_price_diff = history.groupby('customer_id')['price'].apply(lambda x: x.iloc[:180].mean() - x.iloc[:180].loc[x['product_code'] == history['product_code'].iloc[0]].mean() if len(x) == 180 else np.nan).reset_index(drop=True)
    X = X.merge(avg_price_diff, left_on='customer_id', right_index=True, suffixes=('', '_avg_price_diff'))

    # Count the number of different sales channels used by each customer in the past 180 days, excluding purchases from the same department
    sales_channels_diff = history['sales_channel_id'].groupby(history['customer_id']).apply(lambda x: x.iloc[:180].nunique() - x.iloc[:180].loc[x['department_no'] == history['department_no'].iloc[0]].nunique() if len(x) == 180 else np.nan).reset_index(drop=True)
    X = X.merge(sales_channels_diff, left_on='customer_id', right_index=True, suffixes=('', '_sales_channels_diff'))

    # Select the generated features
    f_features = ['f_avg_price', 'f_prod_cat', 'f_dept_purchases', 'f_avg_time_between_purchases', 
                  'f_sales_channels', 'f_prod_cat_ratio', 'f_avg_age', 'f_avg_articles_purchased', 
                  'f_dept_proportion', 'f_avg_price_diff', 'f_sales_channels_diff']
    
    # Return the DataFrame with the generated features
    X = X[f_features + list(X.columns)]
    return X
