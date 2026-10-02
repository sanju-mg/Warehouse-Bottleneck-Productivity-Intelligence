-- ============================================================================
-- 02_delivery_bottleneck.sql
-- Fulfillment Bottlenecks & SLA Variance Analysis
-- ============================================================================

USE supply_chain_intelligence;

-- 1. SLA Performance & Delivery Status Breakdown
SELECT 
    delivery_status,
    COUNT(order_item_id) AS item_count,
    ROUND(COUNT(order_item_id) * 100.0 / (SELECT COUNT(*) FROM dataco_fulfillment), 2) AS status_share_pct,
    ROUND(AVG(actual_shipping_days), 2) AS avg_actual_days,
    ROUND(AVG(scheduled_shipping_days), 2) AS avg_scheduled_days,
    ROUND(AVG(shipping_delay_days), 2) AS avg_delay_days,
    ROUND(SUM(sales), 2) AS total_sales_exposure
FROM dataco_fulfillment
GROUP BY delivery_status
ORDER BY item_count DESC;

-- 2. Shipping Delay Days Distribution (SLA Variance Bins)
SELECT 
    CASE 
        WHEN shipping_delay_days < 0 THEN 'Early Delivery (< 0 Days)'
        WHEN shipping_delay_days = 0 THEN 'On Time (0 Days Variance)'
        WHEN shipping_delay_days = 1 THEN 'Minor Delay (+1 Day)'
        WHEN shipping_delay_days = 2 THEN 'Moderate Delay (+2 Days)'
        WHEN shipping_delay_days >= 3 THEN 'Critical Delay (>= +3 Days)'
    END AS delay_severity_category,
    COUNT(order_item_id) AS item_count,
    ROUND(COUNT(order_item_id) * 100.0 / (SELECT COUNT(*) FROM dataco_fulfillment), 2) AS pct_share,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(order_profit_per_order), 2) AS total_profit
FROM dataco_fulfillment
GROUP BY 
    CASE 
        WHEN shipping_delay_days < 0 THEN 'Early Delivery (< 0 Days)'
        WHEN shipping_delay_days = 0 THEN 'On Time (0 Days Variance)'
        WHEN shipping_delay_days = 1 THEN 'Minor Delay (+1 Day)'
        WHEN shipping_delay_days = 2 THEN 'Moderate Delay (+2 Days)'
        WHEN shipping_delay_days >= 3 THEN 'Critical Delay (>= +3 Days)'
    END
ORDER BY MIN(shipping_delay_days);

-- 3. Quantity vs Delay Severity Analysis
SELECT 
    order_item_quantity,
    COUNT(order_item_id) AS line_item_count,
    ROUND(AVG(actual_shipping_days), 2) AS avg_actual_days,
    ROUND(AVG(shipping_delay_days), 2) AS avg_delay_days,
    ROUND(AVG(late_delivery_flag) * 100, 2) AS late_delivery_rate_pct
FROM dataco_fulfillment
GROUP BY order_item_quantity
ORDER BY order_item_quantity;
