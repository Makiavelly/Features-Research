def modify_features(X, history):
    # Compute past purchase price average by customer
    past_price_avg = history.pivot_table(index="customer_id", values="price", aggfunc="mean")
    past_price_avg = past_price_avg.rename(columns={"price": "f_past_price_avg"})

    # Compute past purchase count by customer and article
    past_count_avg = history.pivot_table(index="customer_id", values="days_ago", aggfunc="count")
    past_count_avg = past_count_avg.rename(columns={"days_ago": "f_past_count_avg"})

    # Compute article type average by customer
    article_type_avg = history.pivot_table(index="customer_id", values="product_type_no", aggfunc="mean")
    article_type_avg = article_type_avg.rename(columns={"product_type_no": "f_article_type_avg"})

    # Compute interaction between past purchase price and article type
    past_price_avg_product_type_no = pd.merge(history, past_price_avg, on="customer_id")[['customer_id', 'price', 'product_type_no']].groupby(['customer_id', 'product_type_no']).agg(lambda x: x['price'].mean()).rename(columns={'price': 'f_past_price_avg_product_type_no'})
    
    # Merge aggregations with X on customer_id
    F = pd.merge(X, past_price_avg.reset_index(), on="customer_id", validate='many_to_one')
    F = pd.merge(F, past_count_avg.reset_index(), on=["customer_id", "article_id"], validate='many_to_one')
    F = pd.merge(F, article_type_avg.reset_index(), on="customer_id", validate='many_to_one')
    F = pd.merge(F, past_price_avg_product_type_no.reset_index(), on=['customer_id', 'product_type_no'], validate='many_to_one')

    # Preserve left ordering after join
    F = F.sort_index()

    # Drop unnecessary columns
    F = F.drop(columns=['price', 'customer_age', 'product_type_no', 'days_ago'])

    # Reorder columns
    F = F[['customer_id', 'article_id', 'raw_u_age', 'raw_u_fn', 'raw_u_active', 'raw_u_club_member_status', 'raw_u_fashion_news_frequency', 'raw_i_product_code', 'raw_i_graphical_appearance_no', 'raw_i_colour_group_code', 'raw_i_perceived_colour_value_id', 'raw_i_perceived_colour_master_id', 'raw_i_department_no', 'raw_i_index_group_no', 'raw_i_section_no', 'raw_i_garment_group_no', 'f_past_price_avg', 'f_past_count_avg', 'f_article_type_avg', 'f_past_price_avg_product_type_no']]

    return F
