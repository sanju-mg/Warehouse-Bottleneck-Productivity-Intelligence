-- ============================================================================
-- WAREHOUSE BOTTLENECK & PRODUCTIVITY INTELLIGENCE
-- MySQL 8.0 Database Schema Definition & Bulk Data Ingestion Script
-- Synchronized with data/processed/analytics/dataco_featured.csv (79 Columns)
-- ============================================================================

CREATE DATABASE IF NOT EXISTS supply_chain_intelligence;
USE supply_chain_intelligence;

DROP TABLE IF EXISTS dataco_fulfillment;

CREATE TABLE dataco_fulfillment (
    -- 1. Transaction & Basic Demographics (Cols 1-6)
    transaction_type VARCHAR(50),
    actual_shipping_days INT NOT NULL,
    scheduled_shipping_days INT NOT NULL,
    benefit_per_order DECIMAL(12, 4) NOT NULL,
    sales_per_customer DECIMAL(12, 4) NOT NULL,
    delivery_status VARCHAR(50) NOT NULL,
    
    -- 2. Initial Risk & Category Hierarchy (Cols 7-11)
    late_delivery_risk TINYINT(1) NOT NULL,
    category_id INT NOT NULL,
    category_name VARCHAR(100) NOT NULL,
    customer_city VARCHAR(100) NOT NULL,
    customer_country VARCHAR(100) NOT NULL,
    
    -- 3. Customer Demographics & Address (Cols 12-18)
    customer_fname VARCHAR(50),
    customer_id INT NOT NULL,
    customer_lname VARCHAR(50),
    customer_segment VARCHAR(50) NOT NULL,
    customer_state VARCHAR(50) NOT NULL,
    customer_street VARCHAR(255) NOT NULL,
    customer_zipcode INT NOT NULL,
    
    -- 4. Department & Location Coordinates (Cols 19-25)
    department_id INT NOT NULL,
    department_name VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    market VARCHAR(50) NOT NULL,
    order_city VARCHAR(100) NOT NULL,
    order_country VARCHAR(100) NOT NULL,
    
    -- 5. Order & Item Keys (Cols 26-32)
    order_customer_id INT NOT NULL,
    order_date DATETIME NOT NULL,
    order_id INT NOT NULL,
    order_item_cardprod_id INT NOT NULL,
    order_item_discount DECIMAL(12, 4) NOT NULL,
    order_item_discount_rate DECIMAL(7, 4) NOT NULL,
    order_item_id INT NOT NULL PRIMARY KEY,
    
    -- 6. Financials & Quantities (Cols 33-38)
    order_item_product_price DECIMAL(12, 4) NOT NULL,
    order_item_profit_ratio DECIMAL(7, 4) NOT NULL,
    order_item_quantity INT NOT NULL,
    sales DECIMAL(12, 4) NOT NULL,
    order_item_total DECIMAL(12, 4) NOT NULL,
    order_profit_per_order DECIMAL(12, 4) NOT NULL,
    
    -- 7. Logistics Destination & Catalog (Cols 39-47)
    order_region VARCHAR(100) NOT NULL,
    order_state VARCHAR(100) NOT NULL,
    order_status VARCHAR(50) NOT NULL,
    order_zipcode VARCHAR(20) NOT NULL,
    product_card_id INT NOT NULL,
    product_category_id INT NOT NULL,
    product_image VARCHAR(255),
    product_name VARCHAR(255) NOT NULL,
    product_price DECIMAL(12, 4) NOT NULL,
    
    -- 8. Shipping Dates & Delay Flags (Cols 48-55)
    shipping_date DATETIME NOT NULL,
    shipping_mode VARCHAR(50) NOT NULL,
    shipping_delay_days INT NOT NULL,
    late_delivery_flag TINYINT(1) NOT NULL,
    on_time_flag TINYINT(1) NOT NULL,
    early_delivery_flag TINYINT(1) NOT NULL,
    canceled_flag TINYINT(1) NOT NULL,
    delivery_performance_category VARCHAR(20) NOT NULL,
    
    -- 9. Temporal Features (Cols 56-64)
    order_year INT NOT NULL,
    order_month INT NOT NULL,
    order_quarter INT NOT NULL,
    order_week INT NOT NULL,
    order_day INT NOT NULL,
    order_weekday VARCHAR(15) NOT NULL,
    order_hour INT NOT NULL,
    order_year_month VARCHAR(7) NOT NULL,
    is_weekend TINYINT(1) NOT NULL,
    
    -- 10. Financial & Unit Derived Metrics (Cols 65-72)
    order_quantity INT NOT NULL,
    quantity_per_order INT NOT NULL,
    order_value DECIMAL(12, 4) NOT NULL,
    order_profit DECIMAL(12, 4) NOT NULL,
    discount_rate DECIMAL(7, 4) NOT NULL,
    profit_margin DECIMAL(7, 4) NOT NULL,
    revenue_per_unit DECIMAL(12, 4) NOT NULL,
    shipping_delay_risk TINYINT(1) NOT NULL,
    
    -- 11. Operational Risk Scores & Aggregates (Cols 73-79)
    high_delay_flag TINYINT(1) DEFAULT 0,
    critical_delay_flag TINYINT(1) DEFAULT 0,
    category_delay_rate DECIMAL(7, 4),
    category_volume INT,
    region_delay_rate DECIMAL(7, 4),
    shipping_mode_risk DECIMAL(7, 4),
    composite_risk_score DECIMAL(7, 4),
    
    -- Indexes for High-Performance Analytics Queries
    INDEX idx_order_id (order_id),
    INDEX idx_order_item_id (order_item_id),
    INDEX idx_customer_id (customer_id),
    INDEX idx_product_card_id (product_card_id),
    INDEX idx_shipping_mode (shipping_mode),
    INDEX idx_delivery_status (delivery_status),
    INDEX idx_order_region (order_region),
    INDEX idx_order_country (order_country),
    INDEX idx_order_date (order_date),
    INDEX idx_category_name (category_name),
    INDEX idx_late_delivery_risk (late_delivery_risk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- BULK DATA IMPORT COMMAND (TASK 3)
-- Execute this statement in MySQL Client / Workbench to import dataco_featured.csv
-- ============================================================================

/*
LOAD DATA LOCAL INFILE 'g:/Warehouse-Bottleneck-Productivity-Intelligence/data/processed/analytics/dataco_featured.csv'
INTO TABLE dataco_fulfillment
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
*/
