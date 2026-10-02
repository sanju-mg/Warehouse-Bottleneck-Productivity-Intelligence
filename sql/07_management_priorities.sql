-- ============================================================================
-- 07_management_priorities.sql
-- Management Intervention Priority Ranking via Composite Operational Risk Score
--
-- METHODOLOGY NOTE:
-- The Operational Risk Score is an analyst-defined composite scoring index (0 - 100)
-- designed to prioritize executive resource allocation across operational entities.
-- Weights:
--   - 40%: Late-Delivery Rate (norm_late_rate)
--   - 30%: Average Shipping Delay Duration (norm_delay)
--   - 30%: Total Order Line Item Volume (norm_volume)
-- ============================================================================

USE supply_chain_intelligence;

-- 1. Management Priority Matrix: Regional Operational Risk Score
WITH regional_raw AS (
    SELECT 
        market,
        order_region,
        COUNT(order_item_id) AS item_volume,
        AVG(late_delivery_flag) AS late_rate,
        AVG(shipping_delay_days) AS avg_delay_days,
        SUM(sales) AS total_sales
    FROM dataco_fulfillment
    GROUP BY market, order_region
),
regional_stats AS (
    SELECT 
        market,
        order_region,
        item_volume,
        late_rate,
        avg_delay_days,
        total_sales,
        (item_volume - MIN(item_volume) OVER()) / (MAX(item_volume) OVER() - MIN(item_volume) OVER()) AS norm_volume,
        (late_rate - MIN(late_rate) OVER()) / (MAX(late_rate) OVER() - MIN(late_rate) OVER()) AS norm_late_rate,
        (avg_delay_days - MIN(avg_delay_days) OVER()) / (MAX(avg_delay_days) OVER() - MIN(avg_delay_days) OVER()) AS norm_delay
    FROM regional_raw
)
SELECT 
    order_region,
    market,
    item_volume,
    ROUND(late_rate * 100, 2) AS late_delivery_rate_pct,
    ROUND(avg_delay_days, 2) AS avg_shipping_variance_days,
    ROUND(total_sales, 2) AS total_sales,
    ROUND((norm_late_rate * 0.4 + norm_delay * 0.3 + norm_volume * 0.3) * 100, 2) AS operational_risk_score,
    DENSE_RANK() OVER (ORDER BY (norm_late_rate * 0.4 + norm_delay * 0.3 + norm_volume * 0.3) DESC) AS priority_rank
FROM regional_stats
ORDER BY priority_rank;

-- 2. Management Priority Matrix: Product Category Risk Ranking
WITH category_raw AS (
    SELECT 
        category_name,
        department_name,
        COUNT(order_item_id) AS item_volume,
        AVG(late_delivery_flag) AS late_rate,
        AVG(shipping_delay_days) AS avg_delay_days,
        SUM(sales) AS total_sales
    FROM dataco_fulfillment
    GROUP BY category_name, department_name
),
category_stats AS (
    SELECT 
        category_name,
        department_name,
        item_volume,
        late_rate,
        avg_delay_days,
        total_sales,
        (item_volume - MIN(item_volume) OVER()) / (MAX(item_volume) OVER() - MIN(item_volume) OVER()) AS norm_volume,
        (late_rate - MIN(late_rate) OVER()) / (MAX(late_rate) OVER() - MIN(late_rate) OVER()) AS norm_late_rate,
        (avg_delay_days - MIN(avg_delay_days) OVER()) / (MAX(avg_delay_days) OVER() - MIN(avg_delay_days) OVER()) AS norm_delay
    FROM category_raw
)
SELECT 
    category_name,
    department_name,
    item_volume,
    ROUND(late_rate * 100, 2) AS late_delivery_rate_pct,
    ROUND(avg_delay_days, 2) AS avg_shipping_variance_days,
    ROUND(total_sales, 2) AS total_sales,
    ROUND((norm_late_rate * 0.4 + norm_delay * 0.3 + norm_volume * 0.3) * 100, 2) AS operational_risk_score,
    DENSE_RANK() OVER (ORDER BY (norm_late_rate * 0.4 + norm_delay * 0.3 + norm_volume * 0.3) DESC) AS priority_rank
FROM category_stats
ORDER BY priority_rank
LIMIT 15;
