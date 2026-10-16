def modify_features(X, history):
    #Compute past purchase price average by customer
    past_price_avg = history.groupby('customer_id')['price'].mean().reset_index()
    past_price_avg = past_price_avg.rename(columns={"price": "f_past_price_avg"})

    #Compute past purchase count by customer
    past_count_avg = history.groupby('customer_id')['days_ago'].count().reset_index()
    past_count_avg = past_count_avg.rename(columns={"days_ago": "f_past_count_avg"})

    #Compute article type average by customer
    article_type_avg = history.groupby('customer_id')['product_type_no'].mean().reset_index()
    article_type_avg = article_type_avg.rename(columns={"product_type_no": "f_article_type_avg"})

    #Compute interaction between past purchase price and article type
    past_price_avg_product_type_no = history.groupby(['customer_id', 'product_type_no'])['price'].mean().reset_index()
    past_price_avg_product_type_no = past_price_avg_product_type_no.rename(columns={"price": "f_past_price_avg_product_type_no"})

    #Filter days_ago for calendar-day windows
    history = history[history['days_ago'] <= 180]

    #Filter days_ago for specific segments
    history = history[history['customer_age'] > 18] # Filter out customers under 18

    #Merge aggregations with X on customer_id
    F = pd.merge(X, past_price_avg[['customer_id', 'f_past_price_avg']].drop_duplicates(), on="customer_id", validate='many_to_one', how="left")
    F = pd.merge(F, past_count_avg[['customer_id', 'article_id', 'f_past_count_avg']].drop_duplicates(), on=["customer_id", "article_id"], validate='many_to_one', how="left")
    F = pd.merge(F, article_type_avg[['customer_id', 'f_article_type_avg']].drop_duplicates(), on="customer_id", validate='many_to_one', how="left")
    F = pd.merge(F, past_price_avg_product_type_no[['customer_id', 'product_type_no', 'f_past_price_avg_product_type_no']], on=['customer_id', 'product_type_no'], how="left", validate='many_to_one')

    #Drop unnecessary columns
    F = F.drop(columns=['price', 'customer_age', 'product_type_no', 'days_ago'])

    #Reorder columns
    F = F[ X.columns.tolist() + [col for col in F.columns if col not in X.columns ]]

    return F
