-- ============================================================================
-- 05_product_category_analysis.sql
-- Product, Category & Department Operational Fulfillment Analysis
-- ============================================================================

USE supply_chain_intelligence;

-- 1. Department Performance Ranking
SELECT 
    department_id,
    department_name,
    COUNT(order_item_id) AS total_order_items,
    SUM(order_item_quantity) AS total_quantity,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(order_profit_per_order), 2) AS total_profit,
    ROUND(AVG(actual_shipping_days), 2) AS avg_actual_days,
    ROUND(AVG(shipping_delay_days), 2) AS avg_delay_days,
    ROUND(AVG(late_delivery_flag) * 100, 2) AS late_delivery_rate_pct
FROM dataco_fulfillment
GROUP BY department_id, department_name
ORDER BY late_delivery_rate_pct DESC;

-- 2. Top 15 Product Categories by Volume & Late Delivery Rate
SELECT 
    category_id,
    category_name,
    department_name,
    COUNT(order_item_id) AS total_order_items,
    SUM(order_item_quantity) AS total_quantity,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(order_profit_per_order), 2) AS total_profit,
    ROUND(AVG(shipping_delay_days), 2) AS avg_delay_days,
    ROUND(AVG(late_delivery_flag) * 100, 2) AS late_delivery_rate_pct,
    DENSE_RANK() OVER (ORDER BY COUNT(order_item_id) DESC) AS rank_by_volume,
    DENSE_RANK() OVER (ORDER BY AVG(late_delivery_flag) DESC) AS rank_by_late_rate
FROM dataco_fulfillment
GROUP BY category_id, category_name, department_name
ORDER BY total_order_items DESC
LIMIT 15;

-- 3. Top Delayed Products (Volume >= 200 Items)
SELECT 
    product_card_id,
    product_name,
    category_name,
    COUNT(order_item_id) AS total_order_items,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(shipping_delay_days), 2) AS avg_delay_days,
    ROUND(AVG(late_delivery_flag) * 100, 2) AS late_delivery_rate_pct
FROM dataco_fulfillment
GROUP BY product_card_id, product_name, category_name
HAVING COUNT(order_item_id) >= 200
ORDER BY late_delivery_rate_pct DESC, total_order_items DESC
LIMIT 15;
