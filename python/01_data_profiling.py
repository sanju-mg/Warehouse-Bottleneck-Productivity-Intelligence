"""
01_data_profiling.py
Warehouse Bottleneck & Productivity Intelligence
Data Profiling & Initial Inspection Script
"""

import os
import pandas as pd
import numpy as np

def run_data_profiling():
    raw_path = "data/raw/DataCoSupplyChainDataset.csv"
    desc_path = "data/raw/DescriptionDataCoSupplyChain.csv"
    
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw dataset not found at {raw_path}")
        
    print("Loading raw dataset for profiling...")
    df = pd.read_csv(raw_path, encoding="ISO-8859-1")
    file_size_mb = os.path.getsize(raw_path) / (1024 * 1024)
    
    # 1. Dataset Shape & Grain
    total_rows, total_cols = df.shape
    distinct_orders = df["Order Id"].nunique()
    distinct_items = df["Order Item Id"].nunique()
    distinct_customers = df["Order Customer Id"].nunique()
    distinct_products = df["Product Card Id"].nunique()
    distinct_categories = df["Category Id"].nunique()
    distinct_category_names = df["Category Name"].nunique()
    distinct_departments = df["Department Id"].nunique()
    distinct_markets = df["Market"].nunique()
    distinct_regions = df["Order Region"].nunique()
    distinct_countries = df["Order Country"].nunique()
    distinct_cities = df["Order City"].nunique()
    distinct_shipping_modes = df["Shipping Mode"].nunique()
    
    # Date Range
    df['order_date_dt'] = pd.to_datetime(df['order date (DateOrders)'])
    df['shipping_date_dt'] = pd.to_datetime(df['shipping date (DateOrders)'])
    
    min_order_date = df['order_date_dt'].min()
    max_order_date = df['order_date_dt'].max()
    min_ship_date = df['shipping_date_dt'].min()
    max_ship_date = df['shipping_date_dt'].max()
    
    # Missing Values
    null_counts = df.isnull().sum()
    null_pcts = (null_counts / total_rows) * 100
    null_df = pd.DataFrame({'Null Count': null_counts, 'Null Percentage': null_pcts})
    high_nulls = null_df[null_df['Null Count'] > 0]
    
    # Duplicate rows & IDs
    dup_rows = df.duplicated().sum()
    dup_order_ids = total_rows - distinct_orders
    dup_item_ids = total_rows - distinct_items
    
    # Constant columns (zero variance)
    constant_cols = [col for col in df.columns if df[col].nunique(dropna=False) <= 1]
    
    # Shipping & Performance Stats
    df['shipping_variance'] = df['Days for shipping (real)'] - df['Days for shipment (scheduled)']
    avg_real_days = df['Days for shipping (real)'].mean()
    avg_sched_days = df['Days for shipment (scheduled)'].mean()
    avg_variance = df['shipping_variance'].mean()
    late_delivery_count = (df['Delivery Status'] == 'Late delivery').sum()
    late_delivery_pct = (late_delivery_count / total_rows) * 100
    
    print("\n--- DATA PROFILING SUMMARY ---")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Total Rows (Order-Items): {total_rows:,}")
    print(f"Total Columns: {total_cols}")
    print(f"Distinct Orders: {distinct_orders:,}")
    print(f"Distinct Customers: {distinct_customers:,}")
    print(f"Distinct Products: {distinct_products:,}")
    print(f"Distinct Categories: {distinct_categories} (Names: {distinct_category_names})")
    print(f"Distinct Regions: {distinct_regions}")
    print(f"Distinct Countries: {distinct_countries}")
    print(f"Order Date Range: {min_order_date} to {max_order_date}")
    print(f"Late Delivery Rate: {late_delivery_pct:.2f}% ({late_delivery_count:,} items)")
    print(f"Average Actual Shipping Days: {avg_real_days:.2f}")
    print(f"Average Scheduled Shipping Days: {avg_sched_days:.2f}")
    print(f"Average Shipping Variance: {avg_variance:.2f} days")
    print(f"Constant Columns: {constant_cols}")
    
    # Generate docs/data_profile.md
    os.makedirs("docs", exist_ok=True)
    with open("docs/data_profile.md", "w", encoding="utf-8") as f:
        f.write("# Dataset Profile: DataCo Smart Supply Chain\n\n")
        f.write("## Executive Summary & Data Grain\n")
        f.write("- **Primary File**: `DataCoSupplyChainDataset.csv`\n")
        f.write(f"- **File Size**: `{file_size_mb:.2f} MB`\n")
        f.write(f"- **Total Row Count**: `{total_rows:,}`\n")
        f.write(f"- **Total Column Count**: `{total_cols}`\n")
        f.write("- **Dataset Grain**: **Order-Item Level**. Each record represents an individual line item inside a customer order. Multiple rows share the same `Order Id`.\n\n")
        
        f.write("## Key Entity Metrics\n")
        f.write(f"- **Distinct Orders**: `{distinct_orders:,}`\n")
        f.write(f"- **Distinct Order Items**: `{distinct_items:,}`\n")
        f.write(f"- **Distinct Customers**: `{distinct_customers:,}`\n")
        f.write(f"- **Distinct Products**: `{distinct_products:,}`\n")
        f.write(f"- **Distinct Product Categories**: `{distinct_categories}` (Category Names: `{distinct_category_names}`)\n")
        f.write(f"- **Distinct Departments**: `{distinct_departments}`\n")
        f.write(f"- **Distinct Geographic Markets**: `{distinct_markets}`\n")
        f.write(f"- **Distinct Order Regions**: `{distinct_regions}`\n")
        f.write(f"- **Distinct Order Countries**: `{distinct_countries}`\n")
        f.write(f"- **Distinct Order Cities**: `{distinct_cities:,}`\n")
        f.write(f"- **Distinct Shipping Modes**: `{distinct_shipping_modes}`\n\n")
        
        f.write("## Temporal Scope\n")
        f.write(f"- **Order Date Min**: `{min_order_date}`\n")
        f.write(f"- **Order Date Max**: `{max_order_date}`\n")
        f.write(f"- **Shipping Date Min**: `{min_ship_date}`\n")
        f.write(f"- **Shipping Date Max**: `{max_ship_date}`\n\n")
        
        f.write("## Initial Operational Baseline\n")
        f.write(f"- **Late Delivery Rate**: `{late_delivery_pct:.2f}%` (`{late_delivery_count:,}` items)\n")
        f.write(f"- **Average Actual Shipping Time**: `{avg_real_days:.2f}` days\n")
        f.write(f"- **Average Scheduled Shipping Time**: `{avg_sched_days:.2f}` days\n")
        f.write(f"- **Average Shipping Variance**: `{avg_variance:.2f}` days\n\n")
        
        f.write("## Missing Values Analysis\n\n")
        f.write("| Column Name | Missing Count | Missing Percentage |\n")
        f.write("|---|---|---|\n")
        for col, row in high_nulls.iterrows():
            f.write(f"| `{col}` | `{int(row['Null Count']):,}` | `{row['Null Percentage']:.2f}%` |\n")
            
        f.write("\n## Zero-Variance / Constant Columns\n")
        for col in constant_cols:
            f.write(f"- `{col}` (Value: `{df[col].iloc[0]}`)\n")
            
        f.write("\n## Delivery Status Distribution\n\n")
        f.write("| Delivery Status | Order-Item Count | Percentage |\n")
        f.write("|---|---|---|\n")
        ds_vc = df['Delivery Status'].value_counts()
        for status, cnt in ds_vc.items():
            f.write(f"| `{status}` | `{cnt:,}` | `{cnt/total_rows*100:.2f}%` |\n")

    print("Successfully written docs/data_profile.md")

    # Generate docs/data_dictionary.md
    with open("docs/data_dictionary.md", "w", encoding="utf-8") as f:
        f.write("# Data Dictionary: DataCo Supply Chain Dataset\n\n")
        f.write("This document defines the 53 original attributes in `DataCoSupplyChainDataset.csv` and their operational definitions.\n\n")
        f.write("| Column Name | Data Type | Null Count | Unique Values | Operational Description |\n")
        f.write("|---|---|---|---|---|\n")
        for col in df.columns:
            if col in ['order_date_dt', 'shipping_date_dt', 'shipping_variance']:
                continue
            dtype = str(df[col].dtype)
            nulls = int(df[col].isnull().sum())
            uniques = int(df[col].nunique())
            f.write(f"| `{col}` | `{dtype}` | `{nulls:,}` | `{uniques:,}` | Attribute of DataCo Supply Chain dataset |\n")

    print("Successfully written docs/data_dictionary.md")

if __name__ == "__main__":
    run_data_profiling()
