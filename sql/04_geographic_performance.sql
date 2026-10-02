-- ============================================================================
-- 04_geographic_performance.sql
-- Geographic & Regional Logistics Bottleneck Analysis
-- ============================================================================

USE supply_chain_intelligence;

-- 1. Regional SLA Performance Ranking (23 Regions)
SELECT 
    market,
    order_region,
    COUNT(DISTINCT order_id) AS distinct_orders,
    COUNT(order_item_id) AS total_order_items,
    ROUND(AVG(actual_shipping_days), 2) AS avg_actual_days,
    ROUND(AVG(scheduled_shipping_days), 2) AS avg_scheduled_days,
    ROUND(AVG(shipping_delay_days), 2) AS avg_shipping_variance,
    SUM(late_delivery_flag) AS late_items,
    ROUND(AVG(late_delivery_flag) * 100, 2) AS late_delivery_rate_pct,
    ROUND(SUM(sales), 2) AS total_sales,
    DENSE_RANK() OVER (ORDER BY AVG(late_delivery_flag) DESC) AS rank_by_late_rate
FROM dataco_fulfillment
GROUP BY market, order_region
ORDER BY late_delivery_rate_pct DESC;

-- 2. Top 15 Problematic Destination Countries (Volume >= 500 Order Items)
SELECT 
    order_country,
    order_region,
    COUNT(order_item_id) AS total_order_items,
    ROUND(AVG(actual_shipping_days), 2) AS avg_actual_days,
    ROUND(AVG(shipping_delay_days), 2) AS avg_delay_days,
    ROUND(AVG(late_delivery_flag) * 100, 2) AS late_delivery_rate_pct,
    ROUND(SUM(sales), 2) AS total_sales
FROM dataco_fulfillment
GROUP BY order_country, order_region
HAVING COUNT(order_item_id) >= 500
ORDER BY late_delivery_rate_pct DESC
LIMIT 15;

-- 3. Top 15 Highest Volume Destination Cities with High Delay Rates
SELECT 
    order_city,
    order_state,
    order_country,
    COUNT(order_item_id) AS total_order_items,
    ROUND(AVG(shipping_delay_days), 2) AS avg_delay_days,
    ROUND(AVG(late_delivery_flag) * 100, 2) AS late_delivery_rate_pct
FROM dataco_fulfillment
GROUP BY order_city, order_state, order_country
HAVING COUNT(order_item_id) >= 200
ORDER BY late_delivery_rate_pct DESC, total_order_items DESC
LIMIT 15;
