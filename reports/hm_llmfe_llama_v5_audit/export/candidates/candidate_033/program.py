def modify_features(X, history):
    # Compute avg past purchase price and avg customer age
    past_price_avg = history.pivot_table(index="customer_id", values="price", aggfunc="mean").rename(columns={"price": "f_past_price_avg"})
    past_age_avg = history.pivot_table(index="customer_id", values="customer_age", aggfunc="mean").rename(columns={"customer_age": "f_past_age_avg"})

    # Compute avg past purchase count per customer and article type
    past_count_avg = history.pivot_table(index=["customer_id", "article_id"], values="days_ago", aggfunc="count").rename(columns={"days_ago": "f_past_count_avg"})

    # Merge aggregations with X on customer_id
    past_price_avg = past_price_avg.join(X.set_index("customer_id"), how="left", validate="many_to_one")
    past_age_avg = past_age_avg.join(X.set_index("customer_id"), how="left", validate="many_to_one")
    past_count_avg = past_count_avg.join(X.set_index("customer_id"), how="left", validate="many_to_one").join(X.set_index("article_id"), how="left", validate="many_to_one")

    # Compute interactions between past purchase price and article type
    past_price_slider = past_price_avg.join(X.set_index("article_id"), how="left", validate="many_to_one")
    past_price_slider['f_past_price_avg_product_type_no'] = past_price_slider['f_past_price_avg'] * past_price_slider['raw_i_product_type_no']
    past_price_slider = past_price_slider.dropna()

    # Filter days_ago for calendar-day windows
    history_filtered = history[(history['days_ago'] < 180) & (history['days_ago'] >= 0)]

    # Preserve left ordering after join
    past_price_avg = past_price_avg.sort_index()
    past_age_avg = past_age_avg.sort_index()
    past_count_avg = past_count_avg.sort_index()
    past_price_slider = past_price_slider.sort_index()

    # Assign values positionally to F
    F = pd.concat([past_price_avg, past_age_avg, past_count_avg, past_price_slider], axis=1)

    # Drop unnecessary columns
    F = F.drop(columns=[col for col in F.columns if 'price' in col or 'days_ago' in col or 'customer_age' in col])

    # Reorder columns
    F = F[["f_past_price_avg","f_past_age_avg","f_past_count_avg","f_past_price_avg_product_type_no"] + [col for col in F.columns if col not in ["f_past_price_avg","f_past_age_avg","f_past_count_avg","f_past_price_avg_product_type_no"]]]

    return F
