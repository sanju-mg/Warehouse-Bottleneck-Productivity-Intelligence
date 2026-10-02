-- ============================================================================
-- 06_time_analysis.sql
-- Time-Series & Temporal Capacity Bottleneck Analysis
-- ============================================================================

USE supply_chain_intelligence;

-- 1. Monthly Fulfillment Performance with Month-over-Month (MoM) Growth & Window Metrics
WITH monthly_metrics AS (
    SELECT 
        order_year,
        order_month,
        order_year_month,
        COUNT(DISTINCT order_id) AS monthly_orders,
        COUNT(order_item_id) AS monthly_items,
        SUM(late_delivery_flag) AS monthly_late_items,
        ROUND(AVG(late_delivery_flag) * 100, 2) AS late_delivery_rate_pct,
        ROUND(AVG(shipping_delay_days), 2) AS avg_delay_days,
        ROUND(SUM(sales), 2) AS monthly_sales
    FROM dataco_fulfillment
    GROUP BY order_year, order_month, order_year_month
)
SELECT 
    order_year_month,
    monthly_orders,
    monthly_items,
    late_delivery_rate_pct,
    LAG(late_delivery_rate_pct, 1) OVER (ORDER BY order_year_month) AS prev_month_late_rate,
    ROUND(late_delivery_rate_pct - LAG(late_delivery_rate_pct, 1) OVER (ORDER BY order_year_month), 2) AS mom_late_rate_change,
    avg_delay_days,
    ROUND(AVG(late_delivery_rate_pct) OVER (ORDER BY order_year_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS rolling_3m_avg_late_rate,
    monthly_sales
FROM monthly_metrics
ORDER BY order_year_month;

-- 2. Day of Week Operational Load & SLA Variance
SELECT 
    order_weekday,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(order_item_id) AS total_items,
    ROUND(AVG(shipping_delay_days), 2) AS avg_delay_days,
    ROUND(AVG(late_delivery_flag) * 100, 2) AS late_delivery_rate_pct,
    ROUND(SUM(sales), 2) AS total_sales
FROM dataco_fulfillment
GROUP BY order_weekday
ORDER BY FIELD(order_weekday, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');

-- 3. Hour of Day Fulfillment Pressure (Ordering Peak Hours)
SELECT 
    HOUR(order_date) AS order_hour,
    COUNT(order_item_id) AS item_volume,
    ROUND(AVG(late_delivery_flag) * 100, 2) AS late_delivery_rate_pct,
    ROUND(AVG(shipping_delay_days), 2) AS avg_delay_days
FROM dataco_fulfillment
GROUP BY HOUR(order_date)
ORDER BY order_hour;
