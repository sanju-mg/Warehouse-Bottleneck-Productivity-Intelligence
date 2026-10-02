# Warehouse Bottleneck & Productivity Intelligence — Supply Chain Fulfillment & Logistics Bottleneck Analytics

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](python/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange?logo=mysql)](sql/)
[![Power BI](https://img.shields.io/badge/Power_BI-Star_Schema-yellow?logo=powerbi)](powerbi/)
[![Status](https://img.shields.io/badge/Pipeline-Validated_100%25-brightgreen)](#final-validation)

A complete, production-grade **Supply Chain Fulfillment & Logistics Bottleneck Analytics** portfolio project built upon the Kaggle [DataCo Smart Supply Chain Dataset](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis).

> [!IMPORTANT]
> **Operational Positioning & Scope Transparency**:  
> This project focuses strictly on **Supply Chain Fulfillment & Logistics Bottleneck Analytics** using empirical order-item transit data. Because the source dataset does not contain internal warehouse worker timestamps (e.g., picking, packing, forklift queue times), this project **does NOT fabricate synthetic employee productivity metrics**. All operational insights are derived strictly from measurable logistics SLAs, transit durations, carrier modes, and geographic performance.

---

## 1. Business Problem & Executive Objective

Global supply chains face severe delivery SLA degradation due to fulfillment bottlenecks, unrealistic dispatch promise dates, and regional logistics friction. In this logistics network:

- **54.83% of all order items** suffer from late delivery.
- Over **$20.12M in gross revenue** (54.74% of total sales) is exposed to fulfillment delay risk.
- Premium shipping modes (`First Class`, `Second Class`) experience catastrophic late delivery rates (**95.32%** and **76.63%** respectively) due to unrealistic 1-day and 2-day SLA targets.

This project delivers an end-to-end analytics pipeline — spanning **Python data profiling & feature engineering**, **SQL analytical queries**, and a **Power BI 7-Page Enterprise Dashboard** — to pinpoint bottlenecks, evaluate carrier performance, and establish management intervention priorities.

---

## 2. Dataset Overview & Data Grain

- **Primary Source**: Kaggle DataCo Smart Supply Chain Dataset (`DataCoSupplyChainDataset.csv`)
- **Raw File Size**: `91.47 MB`
- **Total Records (Order Lines)**: `180,519`
- **Distinct Orders**: `65,752`
- **Distinct Customers**: `20,652`
- **Distinct Products**: `118`
- **Date Scope**: `2015-01-01` to `2018-01-31` (37 months)

### Data Grain Specification

> [!CAUTION]
> The dataset grain is **ORDER-ITEM LINE LEVEL** (`order_item_id`).  
> A single customer order (`order_id`) can contain multiple line item records (average of ~2.74 lines per order).  
> - **Total Orders** MUST be calculated using `DISTINCTCOUNT(order_id)` or `COUNT(DISTINCT order_id)`.
> - **Total Order Items** is calculated using `COUNT(order_item_id)` or `COUNTROWS()`.

---

## 3. Data Architecture & End-to-End Pipeline

```
[Raw Kaggle Dataset (180,519 rows × 53 cols)]
                     │
                     ▼
[Stage 1: Python Profiling & Quality Audit] (python/01_data_profiling.py)
                     │
                     ▼
[Stage 2: Python Data Cleaning & Standardization] (python/02_data_cleaning.py)
                     │
                     ▼
[Stage 3: Feature Engineering] (python/03_feature_engineering.py)
                     │ → dataco_featured.csv (180,519 rows × 79 cols)
                     │
        ┌────────────┴──────────────────────────┐
        ▼                                       ▼
[Stage 4: Advanced Python Analytics & EDA]   [Stage 5: MySQL Database Analytics Layer]
(04_eda.py, 05_advanced_analytics.py)        (sql/schema.sql, sql/01-07 Queries)
        │                                       │
        └────────────┬──────────────────────────┘
                     ▼
[Stage 6: Power BI Enterprise Star Schema]
(Fact_OrderItems + 5 Conformed Dimensions, DAX Measures, 7 Dashboard Pages)
```

---

## 4. Key Performance Indicators (KPIs)

| KPI | Empirical Value | Formula / Definition |
|---|---|---|
| **Total Orders** | `65,752` | `DISTINCTCOUNT(Fact_OrderItems[order_id])` |
| **Total Order Items** | `180,519` | `COUNT(Fact_OrderItems[order_item_id])` |
| **Total Quantity Shipped** | `384,079 units` | `SUM(Fact_OrderItems[order_item_quantity])` |
| **Total Sales** | `$36,784,735.01` | `SUM(Fact_OrderItems[sales])` |
| **Total Profit** | `$3,966,902.97` | `SUM(Fact_OrderItems[order_profit_per_order])` |
| **Late Delivery Rate** | `54.83%` | `COUNT(Late Items) / Total Order Items` |
| **On-Time Delivery Rate** | `17.84%` | `COUNT(On-Time Items) / Total Order Items` |
| **Early Delivery Rate** | `23.04%` | `COUNT(Early Items) / Total Order Items` |
| **Average Actual Shipping Days** | `3.50 days` | `AVERAGE(Fact_OrderItems[actual_shipping_days])` |
| **Average Scheduled Shipping Days** | `2.93 days` | `AVERAGE(Fact_OrderItems[scheduled_shipping_days])` |
| **Average Shipping Variance (SLA Gap)** | `+0.57 days` | `Actual Shipping Days - Scheduled Shipping Days` |
| **Delayed Sales Exposure** | `$20,126,395.27` | Total revenue tied to late shipments |

---

## 5. Python Data & Advanced Analytics Layer

The `python/` directory contains 5 modular, standalone scripts:

1. [`01_data_profiling.py`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/python/01_data_profiling.py): Inspects raw dataset shape, data types, missing values, and entity counts. Writes [`docs/data_profile.md`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/docs/data_profile.md) and [`docs/data_dictionary.md`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/docs/data_dictionary.md).
2. [`02_data_cleaning.py`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/python/02_data_cleaning.py): Drops 4 uninformative constant columns, handles null zipcodes/names, standardizes column names to snake_case, and writes [`docs/data_quality_report.md`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/docs/data_quality_report.md).
3. [`03_feature_engineering.py`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/python/03_feature_engineering.py): Computes 30 operational features including `shipping_delay_days`, `late_delivery_flag`, `is_weekend`, `profit_margin`, `revenue_per_unit`, `high_delay_flag`, `category_delay_rate`, `region_delay_rate`, and `composite_risk_score`.
4. [`04_eda.py`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/python/04_eda.py): Generates 20 publication-grade EDA charts saved in `data/processed/eda/`.
5. [`05_advanced_analytics.py`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/python/05_advanced_analytics.py): Runs Isolation Forest anomaly detection (3,531 anomalies detected), Z-score outlier screening, and Ridge regression time-series forecasting.

---

## 6. SQL Analytics Suite

The `sql/` directory provides a full database schema and 7 analytics scripts:

- [`schema.sql`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/sql/schema.sql): MySQL DDL defining `dataco_fulfillment` table with indexes on high-frequency analytics columns.
- [`01_operations_overview.sql`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/sql/01_operations_overview.sql): Macro KPI summaries, customer segment breakdowns, and market performance.
- [`02_delivery_bottleneck.sql`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/sql/02_delivery_bottleneck.sql): SLA status distribution, delay severity bins, and quantity-vs-delay analysis.
- [`03_shipping_mode_analysis.sql`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/sql/03_shipping_mode_analysis.sql): Carrier SLA failure ranking and delivery status matrix.
- [`04_geographic_performance.sql`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/sql/04_geographic_performance.sql): 23-region SLA ranking, top problematic destination countries, and city bottlenecks.
- [`05_product_category_analysis.sql`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/sql/05_product_category_analysis.sql): Department and category operational volume vs delay rates.
- [`06_time_analysis.sql`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/sql/06_time_analysis.sql): Monthly trends with 3-month rolling averages, weekday load, and hour-of-day order pressure.
- [`07_management_priorities.sql`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/sql/07_management_priorities.sql): Management priority risk ranking matrix across regions and product categories.

---

## 7. Power BI Dashboard Architecture & Specifications

The `powerbi/` directory defines an enterprise Star Schema model and 7-page dashboard design:

- [`data_model.md`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/powerbi/data_model.md): Star schema specification featuring `Fact_OrderItems` surrounded by `Dim_Date`, `Dim_Customer`, `Dim_Product`, `Dim_Geography`, and `Dim_ShippingMode`.
- [`dax_measures.md`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/powerbi/dax_measures.md): 36 production DAX measures (AOV, Late Delivery %, SLA Gap, Composite Risk Index, and scalar-safe `CONCATENATEX` ranking measures).
- [`dashboard_design.md`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/powerbi/dashboard_design.md): 7-Page visual blueprint (Executive Overview, Bottleneck Intelligence, Shipping Performance, Geographic Operations, Product & Category Operations, Time & Demand Intelligence, Management Action Center).
- [`power_query_steps.md`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/powerbi/power_query_steps.md): M-code transformation steps for importing and modeling the data in Power BI Desktop.
- [`business_insights.md`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/powerbi/business_insights.md): Strategic recommendations for operations management.

---

## 8. Major Business Insights & Strategic Recommendations

1. **Recalibrate First Class & Second Class Promise Dates**:
   - `First Class` scheduled target of 1 day fails in **95.32%** of cases because actual transit takes 2.00 days.
   - *Action*: Update OMS/ERP promise date targets to 2 days for First Class and 4 days for Second Class to align customer expectations with physical transit capabilities.
2. **Mitigate $20.12M Revenue Exposure**:
   - Over 54% of gross sales are associated with delayed deliveries.
   - *Action*: Introduce priority fulfillment routing for high-value orders (`sales >= $300`) to protect core revenue streams.
3. **Target High-Volume Regional Bottlenecks**:
   - `Central America` (27,198 items, 56.40% late) and `Western Europe` (27,009 items, 54.51% late) represent over 30,000 delayed order items.
   - *Action*: Expand regional 3PL logistics hub capacity and pre-clear customs for top destination countries.

---

## 9. Project Scope & Limitations

As detailed in [`docs/limitations.md`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/docs/limitations.md), this dataset does **NOT** contain internal warehouse micro-operational timestamps:
- No picking start/end times or worker IDs.
- No packing line throughput or forklift utilization rates.
- No aisle/zone warehouse layout maps.

All metrics are positioned strictly around **Supply Chain Fulfillment & Logistics Bottleneck Analytics**.

---

## 10. How to Reproduce & Execute the Project

### Prerequisites
- Python 3.10+
- MySQL 8.0+ (optional, for SQL analytics layer)
- Power BI Desktop (for visual dashboard creation)

### Step 1: Clone Repository & Setup Environment
```bash
git clone https://github.com/your-username/Warehouse-Bottleneck-Productivity-Intelligence.git
cd Warehouse-Bottleneck-Productivity-Intelligence
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Obtain Raw Dataset
Download `DataCoSupplyChainDataset.csv` from [Kaggle](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) and place it in `data/raw/`.

### Step 3: Run Python Analytics Pipeline
```bash
python python/01_data_profiling.py
python python/02_data_cleaning.py
python python/03_feature_engineering.py
python python/04_eda.py
python python/05_advanced_analytics.py
```

### Step 4: Run SQL Schema & Analytics (Optional)
Import `sql/schema.sql` into MySQL and execute scripts `01` through `07`.

### Step 5: Power BI Implementation
Follow [`powerbi/power_query_steps.md`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/powerbi/power_query_steps.md) and [`powerbi/dashboard_design.md`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/powerbi/dashboard_design.md) to load `dataco_featured.csv` into Power BI Desktop.

---

## 11. Project Audit & Final Validation

This repository has passed a 100% rigorous validation audit:
- [x] [`docs/project_audit.md`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/docs/project_audit.md): Complete audit of row counts, column types, and missing values.
- [x] [`docs/business_logic.md`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/docs/business_logic.md): Canonical specification of late delivery rules and SLA logic.
- [x] [`docs/final_validation_report.md`](file:///g:/Warehouse-Bottleneck-Productivity-Intelligence/docs/final_validation_report.md): Final PASS sign-off across all 11 validation categories.
