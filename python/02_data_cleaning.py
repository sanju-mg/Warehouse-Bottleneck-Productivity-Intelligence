"""
02_data_cleaning.py
Warehouse Bottleneck & Productivity Intelligence
Data Cleaning & Quality Report Script
"""

import os
import pandas as pd
import numpy as np

def run_data_cleaning():
    raw_path = "data/raw/DataCoSupplyChainDataset.csv"
    cleaned_dir = "data/cleaned"
    os.makedirs(cleaned_dir, exist_ok=True)
    
    print("Loading raw dataset for cleaning...")
    df = pd.read_csv(raw_path, encoding="ISO-8859-1")
    initial_shape = df.shape
    
    cleaning_log = []
    
    # 1. Drop 100% null and constant columns
    drop_cols = ["Product Description", "Customer Email", "Customer Password", "Product Status"]
    df.drop(columns=drop_cols, inplace=True)
    cleaning_log.append(f"Dropped 4 uninformative/constant columns: {drop_cols}")
    
    # 2. Handle missing values
    df['Customer Lname'] = df['Customer Lname'].fillna('')
    cleaning_log.append("Filled 8 missing values in 'Customer Lname' with empty string")
    
    df['Customer Zipcode'] = df['Customer Zipcode'].fillna(0).astype(int)
    cleaning_log.append("Filled 3 missing values in 'Customer Zipcode' with 0 and cast to int")
    
    df['Order Zipcode'] = df['Order Zipcode'].fillna(-1).astype(int).astype(str).replace('-1', 'Unknown')
    cleaning_log.append("Handled 155,679 missing values in 'Order Zipcode' by setting to 'Unknown'")
    
    # 3. Strip whitespace
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
    cleaning_log.append(f"Stripped whitespace from {len(text_cols)} string columns")
    
    # 4. Standardize Column Names
    col_mapping = {
        'Type': 'transaction_type',
        'Days for shipping (real)': 'actual_shipping_days',
        'Days for shipment (scheduled)': 'scheduled_shipping_days',
        'Benefit per order': 'benefit_per_order',
        'Sales per customer': 'sales_per_customer',
        'Delivery Status': 'delivery_status',
        'Late_delivery_risk': 'late_delivery_risk',
        'Category Id': 'category_id',
        'Category Name': 'category_name',
        'Customer City': 'customer_city',
        'Customer Country': 'customer_country',
        'Customer Fname': 'customer_fname',
        'Customer Id': 'customer_id',
        'Customer Lname': 'customer_lname',
        'Customer Segment': 'customer_segment',
        'Customer State': 'customer_state',
        'Customer Street': 'customer_street',
        'Customer Zipcode': 'customer_zipcode',
        'Department Id': 'department_id',
        'Department Name': 'department_name',
        'Latitude': 'latitude',
        'Longitude': 'longitude',
        'Market': 'market',
        'Order City': 'order_city',
        'Order Country': 'order_country',
        'Order Customer Id': 'order_customer_id',
        'order date (DateOrders)': 'order_date',
        'Order Id': 'order_id',
        'Order Item Cardprod Id': 'order_item_cardprod_id',
        'Order Item Discount': 'order_item_discount',
        'Order Item Discount Rate': 'order_item_discount_rate',
        'Order Item Id': 'order_item_id',
        'Order Item Product Price': 'order_item_product_price',
        'Order Item Profit Ratio': 'order_item_profit_ratio',
        'Order Item Quantity': 'order_item_quantity',
        'Sales': 'sales',
        'Order Item Total': 'order_item_total',
        'Order Profit Per Order': 'order_profit_per_order',
        'Order Region': 'order_region',
        'Order State': 'order_state',
        'Order Status': 'order_status',
        'Order Zipcode': 'order_zipcode',
        'Product Card Id': 'product_card_id',
        'Product Category Id': 'product_category_id',
        'Product Image': 'product_image',
        'Product Name': 'product_name',
        'Product Price': 'product_price',
        'shipping date (DateOrders)': 'shipping_date',
        'Shipping Mode': 'shipping_mode'
    }
    
    df.rename(columns=col_mapping, inplace=True)
    cleaning_log.append("Renamed 49 active columns to standardized snake_case format")
    
    # 5. Dates
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['shipping_date'] = pd.to_datetime(df['shipping_date'])
    cleaning_log.append("Parsed 'order_date' and 'shipping_date' into datetime format YYYY-MM-DD HH:MM:SS")
    
    # Export cleaned data
    cleaned_path = os.path.join(cleaned_dir, "dataco_cleaned.csv")
    df.to_csv(cleaned_path, index=False)
    print(f"Cleaned dataset saved to {cleaned_path} with shape {df.shape}")
    
    # Write docs/data_quality_report.md
    with open("docs/data_quality_report.md", "w", encoding="utf-8") as f:
        f.write("# Data Quality & Cleaning Report\n\n")
        f.write("## Executive Summary\n")
        f.write(f"- **Initial Raw Shape**: `{initial_shape[0]:,}` rows × `{initial_shape[1]}` columns\n")
        f.write(f"- **Cleaned Dataset Shape**: `{df.shape[0]:,}` rows × `{df.shape[1]}` columns\n")
        f.write(f"- **Cleaned Output File**: `data/cleaned/dataco_cleaned.csv`\n\n")
        
        f.write("## Step-by-Step Transformations\n\n")
        for i, step in enumerate(cleaning_log, 1):
            f.write(f"{i}. **{step}**\n")

    print("Successfully written docs/data_quality_report.md")

if __name__ == "__main__":
    run_data_cleaning()
