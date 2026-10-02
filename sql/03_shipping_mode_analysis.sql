-- ============================================================================
-- 03_shipping_mode_analysis.sql
-- Carrier & Shipping Mode SLA Performance Ranking
-- ============================================================================

USE supply_chain_intelligence;

-- 1. Comprehensive Shipping Mode SLA & Variance Ranking
SELECT 
    shipping_mode,
    COUNT(DISTINCT order_id) AS distinct_orders,
    COUNT(order_item_id) AS total_order_items,
    ROUND(AVG(scheduled_shipping_days), 2) AS avg_scheduled_days,
    ROUND(AVG(actual_shipping_days), 2) AS avg_actual_days,
    ROUND(AVG(shipping_delay_days), 2) AS avg_sla_gap_days,
    SUM(late_delivery_flag) AS late_item_count,
    ROUND(AVG(late_delivery_flag) * 100, 2) AS late_delivery_rate_pct,
    ROUND(AVG(on_time_flag) * 100, 2) AS on_time_rate_pct,
    ROUND(AVG(early_delivery_flag) * 100, 2) AS early_rate_pct,
    ROUND(SUM(sales), 2) AS total_sales_volume,
    ROUND(SUM(CASE WHEN late_delivery_flag = 1 THEN sales ELSE 0 END), 2) AS delayed_sales_exposure
FROM dataco_fulfillment
GROUP BY shipping_mode
ORDER BY late_delivery_rate_pct DESC;

-- 2. Shipping Mode Delivery Status Matrix
SELECT 
    shipping_mode,
    delivery_status,
    COUNT(order_item_id) AS item_count,
    ROUND(AVG(actual_shipping_days), 2) AS avg_actual_days,
    ROUND(SUM(sales), 2) AS total_sales
FROM dataco_fulfillment
GROUP BY shipping_mode, delivery_status
ORDER BY shipping_mode, item_count DESC;
