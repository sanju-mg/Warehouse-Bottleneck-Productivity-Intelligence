-- ============================================================================
-- 01_operations_overview.sql
-- Operations KPI Summary & Baseline Performance
-- ============================================================================

USE supply_chain_intelligence;

-- 1. Executive Fulfillment KPI Summary
SELECT 
    COUNT(DISTINCT order_id) AS total_unique_orders,
    COUNT(order_item_id) AS total_order_items,
    SUM(order_item_quantity) AS total_quantity_shipped,
    ROUND(SUM(sales), 2) AS total_gross_sales,
    ROUND(SUM(order_profit_per_order), 2) AS total_net_profit,
    COUNT(DISTINCT customer_id) AS total_active_customers,
    COUNT(DISTINCT product_card_id) AS total_active_products,
    ROUND(AVG(sales), 2) AS avg_item_sales_value,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM dataco_fulfillment;

-- 2. Customer Segment Operations Breakdown
SELECT 
    customer_segment,
    COUNT(DISTINCT order_id) AS distinct_orders,
    COUNT(order_item_id) AS order_items,
    SUM(order_item_quantity) AS total_quantity,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS avg_item_sales,
    ROUND(SUM(order_profit_per_order), 2) AS total_profit,
    ROUND(AVG(late_delivery_flag) * 100, 2) AS late_delivery_rate_pct
FROM dataco_fulfillment
GROUP BY customer_segment
ORDER BY total_sales DESC;

-- 3. Market Fulfillment Overview
SELECT 
    market,
    COUNT(DISTINCT order_id) AS unique_orders,
    COUNT(order_item_id) AS order_item_count,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(order_profit_per_order), 2) AS total_profit,
    ROUND(AVG(actual_shipping_days), 2) AS avg_actual_shipping_days,
    ROUND(AVG(scheduled_shipping_days), 2) AS avg_scheduled_shipping_days,
    ROUND(AVG(shipping_delay_days), 2) AS avg_shipping_variance,
    ROUND(AVG(late_delivery_flag) * 100, 2) AS late_delivery_rate_pct
FROM dataco_fulfillment
GROUP BY market
ORDER BY unique_orders DESC;
