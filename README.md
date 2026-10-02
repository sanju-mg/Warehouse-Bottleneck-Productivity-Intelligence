# 📦 Warehouse Bottleneck & Productivity Intelligence

### An End-to-End Supply Chain Analytics Project Using Python, SQL, Machine Learning, and Power BI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Power_BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI">
  <img src="https://img.shields.io/badge/Scikit--learn-Machine_Learning-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/Status-Portfolio_Project-2ECC71?style=for-the-badge" alt="Project Status">
</p>

---

## 📌 Overview

**Warehouse Bottleneck & Productivity Intelligence** is an end-to-end supply chain analytics project that transforms raw logistics data into actionable business insights.

The project analyzes historical supply chain operations to identify delivery bottlenecks, investigate shipping delays, measure regional performance, and understand operational inefficiencies.

It combines **Python, SQL, Machine Learning, and Power BI** to build a complete analytics workflow, from raw data preprocessing to interactive business intelligence dashboards.

The project also incorporates anomaly detection and forecasting to explore unusual shipping behavior and future operational trends.

### 🎯 Objectives

* Analyze historical supply chain and delivery performance.
* Identify bottlenecks and patterns in shipping delays.
* Measure on-time and late delivery rates.
* Compare shipping performance across regions and product categories.
* Identify unusual shipping records using machine learning.
* Forecast monthly order volume and delivery performance.
* Build an interactive Power BI dashboard.
* Support data-driven operational decision-making.

---

## 🛠️ Tech Stack

| Technology       | Application                           |
| ---------------- | ------------------------------------- |
| Python           | Data analysis and automation          |
| Pandas           | Data cleaning and manipulation        |
| NumPy            | Numerical calculations                |
| Matplotlib       | Data visualization                    |
| Seaborn          | Statistical visualization             |
| Scikit-learn     | Machine learning                      |
| Isolation Forest | Anomaly detection                     |
| Ridge Regression | Forecasting                           |
| MySQL            | Relational database                   |
| SQL              | Business analysis and KPI calculation |
| Power BI         | Interactive dashboards                |
| Git & GitHub     | Version control and project hosting   |

---

## 📊 Dataset

**Dataset:** DataCo Smart Supply Chain Dataset

The project uses historical supply chain data containing order information, shipping details, product categories, customer information, and delivery performance.

| Dataset Attribute | Value                       |
| ----------------- | --------------------------- |
| Dataset           | DataCo Smart Supply Chain   |
| Total order items | 180,519                     |
| Total orders      | 65,752                      |
| Historical period | January 2015 – January 2018 |
| Domain            | Supply Chain and Logistics  |
| Data format       | CSV                         |

### Important Dataset Features

* Order ID
* Order Item ID
* Order Date
* Shipping Date
* Scheduled Shipping Days
* Actual Shipping Days
* Shipping Mode
* Product Category
* Department
* Customer Segment
* Market
* Country
* Region
* Sales
* Profit
* Quantity
* Delivery Status

The dataset is used to investigate historical delivery performance and identify patterns associated with shipping delays.

**Note:** This is historical supply chain data, not a live warehouse tracking dataset.

---

## 🏗️ Project Architecture

The project follows a complete data analytics pipeline.

```text
                 RAW DATASET
                      |
                      ▼
               DATA PROFILING
                  (Python)
                      |
                      ▼
                DATA CLEANING
                  (Pandas)
                      |
                      ▼
             FEATURE ENGINEERING
                  (Python)
                      |
                      ▼
          EXPLORATORY DATA ANALYSIS
                      |
                      ▼
              DATA VISUALIZATION
                (20 Charts)
                      |
                      ▼
             ADVANCED ANALYTICS
                      |
             ┌────────┴────────┐
             ▼                 ▼
       ANOMALY DETECTION    FORECASTING
       Isolation Forest   Ridge Regression
             |                 |
             └────────┬────────┘
                      ▼
                MYSQL DATABASE
                      |
                      ▼
                 SQL ANALYSIS
                      |
                      ▼
               POWER BI REPORT
                      |
                      ▼
               BUSINESS INSIGHTS
```

---

## 📁 Project Structure

```text
Warehouse-Bottleneck-Productivity-Intelligence/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   │
│   ├── raw/
│   │   ├── DataCoSupplyChainDataset.csv
│   │   ├── DescriptionDataCoSupplyChain.csv
│   │   ├── README.md
│   │   └── tokenized_access_logs.csv
│   │
│   ├── cleaned/
│   │   └── dataco_cleaned.csv
│   │
│   └── processed/
│       │
│       ├── analytics/
│       │   ├── dataco_anomalies.csv
│       │   ├── dataco_featured.csv
│       │   ├── dataco_forecasts.csv
│       │   └── dataco_monthly_analytics.csv
│       │
│       └── eda/
│           ├── 01_order_volume_trend.png
│           ├── 02_delivery_performance.png
│           ├── 03_shipping_delay_analysis.png
│           └── ... (20 EDA charts)
│
├── python/
│   ├── 01_data_profiling.py
│   ├── 02_data_cleaning.py
│   ├── 03_feature_engineering.py
│   ├── 04_eda.py
│   ├── 05_advanced_analytics.py
│   └── 06_load_mysql.py
│
├── sql/
│   ├── schema.sql
│   ├── 01_operations_overview.sql
│   ├── 02_delivery_bottleneck.sql
│   ├── 03_shipping_mode_analysis.sql
│   ├── 04_geographic_performance.sql
│   ├── 05_product_category_analysis.sql
│   ├── 06_time_analysis.sql
│   └── 07_management_priorities.sql
│
└── powerbi/
    └── Warehouse_Bottleneck_Productivity_Intelligence.pbix
```

---

# 🔄 Project Workflow

## 1. Data Profiling

The first stage examines the raw dataset to understand its structure and quality.

### Activities

* Inspect dataset dimensions.
* Identify column names and data types.
* Analyze missing values.
* Examine duplicate records.
* Generate descriptive statistics.
* Investigate unique values.
* Identify potential data quality issues.

**Objective:** Understand the dataset before cleaning and analysis.

**Script:** `python/01_data_profiling.py`

## 2. Data Cleaning

Python and Pandas are used to prepare the dataset for analysis.

### Activities

* Remove uninformative columns.
* Handle missing values.
* Standardize column names.
* Convert date columns to datetime format.
* Prepare numerical and categorical columns.
* Save the cleaned dataset.

**Output:** `data/cleaned/dataco_cleaned.csv`

**Script:** `python/02_data_cleaning.py`

## 3. Feature Engineering

Feature engineering creates additional variables to measure operational performance.

### Engineered Features

| Feature                | Description                                           |
| ---------------------- | ----------------------------------------------------- |
| `shipping_delay_days`  | Difference between actual and scheduled shipping days |
| `late_delivery_flag`   | Identifies late deliveries                            |
| `on_time_flag`         | Identifies on-time deliveries                         |
| `early_delivery_flag`  | Identifies early deliveries                           |
| `profit_margin`        | Profit divided by sales                               |
| `revenue_per_unit`     | Revenue generated per unit                            |
| `high_delay_flag`      | Identifies delays of at least two days                |
| `critical_delay_flag`  | Identifies delays of at least three days              |
| `category_delay_rate`  | Historical late-delivery rate by category             |
| `region_delay_rate`    | Historical late-delivery rate by region               |
| `composite_risk_score` | Combines selected operational risk indicators         |

These features help analyze delivery delays, profitability, and operational risk.

**Output:** `data/processed/analytics/dataco_featured.csv`

**Script:** `python/03_feature_engineering.py`

**Note:** Historical category and region delay rates are intended for descriptive analysis. If used for predictive modeling, they must be calculated without using information from the prediction target or future records.

## 4. Exploratory Data Analysis (EDA)

Exploratory Data Analysis is used to discover trends, relationships, and unusual patterns in the dataset.

The project generates 20 visualizations using Python.

### EDA Categories

* Monthly order volume
* Delivery performance
* Shipping delay distribution
* Shipping mode comparison
* Geographic performance
* Country-level performance
* Product category analysis
* Department performance
* Customer segment analysis
* Sales and profit analysis
* Monthly delivery trends
* Operational risk distribution

**Output:** `data/processed/eda/`

**Script:** `python/04_eda.py`

## 5. Advanced Analytics

The project uses machine learning and statistical techniques to investigate operational behavior.

### A. Anomaly Detection Using Isolation Forest

Isolation Forest is an unsupervised machine learning algorithm used to identify unusual observations.

The model analyzes selected features, including:

* Shipping time
* Shipping delay
* Sales
* Quantity

The contamination parameter is set to `0.02`, configuring the model to flag approximately 2% of records as anomalies.

**Business applications:**

* Identify unusual shipping records.
* Highlight shipments that require investigation.
* Support operational monitoring.
* Explore unusual patterns in shipping behavior.

Anomalies are not necessarily errors or confirmed failures. They require further investigation.

### B. Statistical Anomaly Detection Using Z-Score

Z-score analysis identifies observations that are unusually far from the mean.

The project flags shipping delays with an absolute Z-score greater than 3.

This provides a statistical method for detecting extreme shipping delays.

### C. Forecasting Using Ridge Regression

Ridge Regression is used to explore future operational trends.

The project forecasts:

* Monthly order-item volume
* Monthly late-delivery volume
* Monthly late-delivery rate

The model generates a six-month forecast using a sequential time index.

**Business applications:**

* Explore future order-volume trends.
* Estimate potential late-delivery volumes.
* Support preliminary operational planning.

The forecasts are exploratory and should be evaluated against a time-based test set before being used for actual business decisions.

**Outputs:**

* `data/processed/analytics/dataco_anomalies.csv`
* `data/processed/analytics/dataco_forecasts.csv`
* `data/processed/analytics/dataco_monthly_analytics.csv`

**Script:** `python/05_advanced_analytics.py`

---

# 🗄️ SQL Analysis

MySQL is used to store and analyze the processed supply chain data.

The project includes a relational database schema and seven SQL analysis scripts.

| SQL File                           | Purpose                                             |
| ---------------------------------- | --------------------------------------------------- |
| `schema.sql`                       | Creates the database tables and schema              |
| `01_operations_overview.sql`       | Calculates overall operational KPIs                 |
| `02_delivery_bottleneck.sql`       | Analyzes delivery delays and bottlenecks            |
| `03_shipping_mode_analysis.sql`    | Compares shipping mode performance                  |
| `04_geographic_performance.sql`    | Analyzes country and regional performance           |
| `05_product_category_analysis.sql` | Investigates product category and department delays |
| `06_time_analysis.sql`             | Examines monthly and weekday trends                 |
| `07_management_priorities.sql`     | Identifies areas for management investigation       |

### SQL Concepts Used

* SELECT and WHERE
* GROUP BY
* ORDER BY
* Aggregate functions
* CASE statements
* Subqueries
* Common Table Expressions (CTEs)
* Window functions
* DENSE_RANK()
* Conditional aggregation
* Indexing

### Business Applications

SQL queries are used to:

* Calculate operational KPIs.
* Compare shipping modes.
* Identify regions with high late-delivery rates.
* Analyze product categories.
* Examine historical delivery trends.
* Prioritize operational areas for further investigation.

**SQL directory:** `sql/`

---

# 📊 Power BI Dashboard

The project includes an interactive Power BI dashboard for exploring supply chain performance.

**Dashboard file:**

`powerbi/Warehouse_Bottleneck_Productivity_Intelligence.pbix`

### Dashboard Pages

| Page                             | Description                                   |
| -------------------------------- | --------------------------------------------- |
| 1. Executive Overview            | Overall supply chain KPIs and performance     |
| 2. Bottleneck Intelligence       | Delivery delays and operational bottlenecks   |
| 3. Shipping Performance          | Shipping mode comparisons                     |
| 4. Geographic Operations         | Regional and country-level performance        |
| 5. Product & Category Operations | Product and department analysis               |
| 6. Time & Demand Intelligence    | Historical trends and forecasts               |
| 7. Management Action Center      | Operational risk and investigation priorities |

### Key Performance Indicators

* Total Orders
* Total Order Items
* Total Sales
* Total Profit
* Late Delivery Rate
* On-Time Delivery Rate
* Average Shipping Time
* Average Shipping Variance

The dashboard is designed to help users explore performance across different operational dimensions.

Open the PBIX file using Microsoft Power BI Desktop.

---

# 📈 Key Performance Indicators

The following are the reported results from the project's historical dataset.

| KPI                                    |          Value |
| -------------------------------------- | -------------: |
| Total Orders                           |         65,752 |
| Total Order Items                      |        180,519 |
| Total Sales                            | $36,784,735.01 |
| Total Profit                           |  $3,966,902.97 |
| Late Delivery Rate                     |         54.83% |
| On-Time Delivery Rate                  |         17.84% |
| Average Actual Shipping Time           |      3.50 days |
| Average Scheduled Shipping Time        |      2.93 days |
| Average Shipping Variance              |      0.57 days |
| Revenue Associated with Late Shipments | $20,126,395.27 |

These metrics describe the historical dataset and should not be interpreted as current warehouse performance.

---

# 💡 Business Questions

This project is designed to answer the following questions:

1. What percentage of shipments are delivered late?
2. Which shipping modes have higher late-delivery rates?
3. Which regions experience more delivery delays?
4. Which product categories are associated with frequent delays?
5. How does delivery performance change over time?
6. How much revenue is associated with late shipments?
7. Which shipments exhibit unusual behavior?
8. What are the historical monthly order trends?
9. Which operational areas should management investigate?
10. How can historical data support delivery planning?

---

# ⚙️ Installation and Setup

Follow these steps to run the project locally.

## Prerequisites

Install the following software:

* Python 3.10 or later
* MySQL Server
* MySQL Workbench (optional)
* Microsoft Power BI Desktop
* Visual Studio Code (recommended)
* Git

## Step 1: Clone the Repository

```bash
git clone https://github.com/sanju/Warehouse-Bottleneck-Productivity-Intelligence.git
```

Navigate to the project directory:

```bash
cd Warehouse-Bottleneck-Productivity-Intelligence
```

## Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Prepare the Dataset

Ensure the original dataset is available at:

```text
data/raw/DataCoSupplyChainDataset.csv
```

If you downloaded the dataset separately, place it in this directory.

Update the file paths in the Python scripts if necessary.

## Step 5: Run the Python Pipeline

Execute the scripts in the following order:

**1. Data profiling**

```bash
python python/01_data_profiling.py
```

**2. Data cleaning**

```bash
python python/02_data_cleaning.py
```

**3. Feature engineering**

```bash
python python/03_feature_engineering.py
```

**4. Exploratory data analysis**

```bash
python python/04_eda.py
```

**5. Advanced analytics**

```bash
python python/05_advanced_analytics.py
```

**6. Load data into MySQL**

```bash
python python/06_load_mysql.py
```

Run each script sequentially and check its output before proceeding.

The scripts may require local path or database configuration adjustments.

---

# 🐬 MySQL Configuration

Start your MySQL Server and create the database.

```sql
CREATE DATABASE warehouse_analytics;
```

Select the database:

```sql
USE warehouse_analytics;
```

Execute the schema file:

```text
sql/schema.sql
```

Configure the database connection in `python/06_load_mysql.py`.

For security, use environment variables to store database credentials instead of committing passwords to GitHub.

Example configuration:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=warehouse_analytics
```

After loading the data, execute the SQL analysis files in the `sql/` directory.

---

# 📂 Project Outputs

| Output            | Location                    | Description                          |
| ----------------- | --------------------------- | ------------------------------------ |
| Cleaned dataset   | `data/cleaned/`             | Cleaned supply chain data            |
| Featured dataset  | `data/processed/analytics/` | Engineered analytical features       |
| Anomaly results   | `data/processed/analytics/` | Records flagged by anomaly detection |
| Forecast results  | `data/processed/analytics/` | Exploratory monthly forecasts        |
| Monthly analytics | `data/processed/analytics/` | Aggregated monthly metrics           |
| EDA charts        | `data/processed/eda/`       | 20 data visualizations               |
| SQL scripts       | `sql/`                      | Database schema and business queries |
| Power BI report   | `powerbi/`                  | Interactive dashboard                |

---

# 🔐 Data Security and Reproducibility

* Do not commit database passwords or other credentials.
* Use environment variables for sensitive configuration.
* Keep the raw dataset unchanged.
* Document the source and license of the dataset.
* Validate data before loading it into MySQL.
* Avoid destructive database operations without backups.
* Use consistent paths for reproducible execution.

---

# ⚠️ Limitations

Although the project includes multiple analytics techniques, it has several limitations:

1. **Historical data:** The dataset covers January 2015 to January 2018 and does not represent live operations.
2. **Productivity measurement:** The project focuses on shipping and delivery performance rather than direct employee productivity.
3. **Anomaly detection:** Anomaly detection identifies unusual records, not confirmed operational failures.
4. **Forecasting:** Ridge Regression uses a simple time index and may not capture seasonal patterns.
5. **Risk scoring:** Composite risk scores depend on analyst-defined features and weights.
6. **Predictive modeling:** Historical delivery statistics must be calculated carefully to avoid target leakage.
7. **Business validation:** The results should be validated against actual operational data before making real-world decisions.

---

# 🚀 Future Improvements

Potential future developments include:

* Implementing ARIMA or other time-series forecasting methods.
* Comparing forecasts using MAE, RMSE, and MAPE.
* Building a supervised model to predict late deliveries.
* Improving risk scores using validated operational outcomes.
* Adding automated data quality checks.
* Developing a scheduled ETL pipeline.
* Deploying the Power BI dashboard to Power BI Service.
* Integrating live shipment tracking data.
* Implementing automated alerts for unusual delivery delays.
* Optimizing SQL queries and dashboard performance.

---

# 🎓 Skills Demonstrated

This project demonstrates practical experience in:

* Python programming
* Data cleaning and preprocessing
* Exploratory data analysis
* Feature engineering
* SQL and MySQL
* Statistical analysis
* Machine learning
* Anomaly detection
* Regression-based forecasting
* Data visualization
* Business intelligence
* KPI development
* Supply chain analytics
* Business problem-solving

---

# 👨‍💻 Author

**Sanju**

Computer Science and Engineering Student

**Areas of Interest:**

* Data Analytics
* Data Science
* Machine Learning
* Business Intelligence
* Python
* SQL

**GitHub:** [sanju](https://github.com/sanju)

**Project Repository:** [Warehouse Bottleneck & Productivity Intelligence](https://github.com/sanju/Warehouse-Bottleneck-Productivity-Intelligence)

---

# 📜 License

This project is developed for educational and portfolio purposes.

The original dataset may have separate licensing and usage conditions. Refer to its original source before redistributing it.

---

<p align="center">
  <b>Warehouse Bottleneck & Productivity Intelligence</b>
  <br>
  Turning Supply Chain Data into Business Insights
  <br><br>
  ⭐ If you find this project useful, consider starring the repository!
</p>
