WITH customer_stats AS (
    SELECT
        customer_id,
        count(*) AS purchases,
        count(*) FILTER (WHERE days_ago <= 30) AS purchases_30d,
        count(*) FILTER (WHERE days_ago <= 7) AS purchases_7d,
        count(DISTINCT article_id) AS distinct_articles,
        avg(days_ago) AS mean_days_ago,
        min(days_ago) AS most_recent_days_ago,
        avg(price) AS mean_price,
        stddev_pop(price) AS price_stddev
    FROM history
    GROUP BY customer_id
)
SELECT
    customer_id,
    purchases AS f_customer_purchase_count,
    purchases_30d AS f_customer_purchase_count_30d,
    purchases_7d AS f_customer_purchase_count_7d,
    purchases_30d / nullif(purchases, 0) AS f_customer_recent_purchase_share,
    distinct_articles AS f_customer_distinct_articles,
    mean_days_ago AS f_customer_mean_days_ago,
    most_recent_days_ago AS f_customer_recency_days,
    mean_price AS f_customer_mean_price,
    price_stddev AS f_customer_price_stddev
FROM customer_stats;

WITH article_stats AS (
    SELECT
        article_id,
        count(*) AS purchases,
        count(*) FILTER (WHERE days_ago <= 30) AS purchases_30d,
        count(*) FILTER (WHERE days_ago <= 7) AS purchases_7d,
        count(DISTINCT customer_id) AS distinct_customers,
        avg(price) AS mean_price,
        min(days_ago) AS most_recent_days_ago
    FROM history
    GROUP BY article_id
)
SELECT
    article_id,
    purchases AS f_article_purchase_count,
    purchases_30d AS f_article_purchase_count_30d,
    purchases_7d AS f_article_purchase_count_7d,
    distinct_customers AS f_article_distinct_customers,
    mean_price AS f_article_mean_price,
    most_recent_days_ago AS f_article_recency_days
FROM article_stats;

WITH pair_stats AS (
    SELECT
        customer_id,
        article_id,
        count(*) AS purchases,
        count(*) FILTER (WHERE days_ago <= 30) AS purchases_30d,
        count(*) FILTER (WHERE days_ago <= 7) AS purchases_7d,
        min(days_ago) AS most_recent_days_ago,
        avg(price) AS mean_price
    FROM history
    GROUP BY customer_id, article_id
)
SELECT
    customer_id,
    article_id,
    purchases AS f_pair_purchase_count,
    purchases_30d AS f_pair_purchase_count_30d,
    purchases_7d AS f_pair_purchase_count_7d,
    most_recent_days_ago AS f_pair_recency_days,
    mean_price AS f_pair_mean_price
FROM pair_stats;