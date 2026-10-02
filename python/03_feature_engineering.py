"""
03_feature_engineering.py
Warehouse Bottleneck & Productivity Intelligence
Operational Feature Engineering Script
"""

import os
import pandas as pd
import numpy as np

def run_feature_engineering():
    cleaned_path = "data/cleaned/dataco_cleaned.csv"
    analytics_dir = "data/processed/analytics"
    os.makedirs(analytics_dir, exist_ok=True)
    
    print("Loading cleaned dataset for feature engineering...")
    df = pd.read_csv(cleaned_path)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['shipping_date'] = pd.to_datetime(df['shipping_date'])
    
    # A. SHIPPING VARIANCE
    df['shipping_delay_days'] = df['actual_shipping_days'] - df['scheduled_shipping_days']
    
    # B. SLA FLAGS
    df['late_delivery_flag'] = df['late_delivery_risk']
    df['on_time_flag'] = (df['delivery_status'] == 'Shipping on time').astype(int)
    df['early_delivery_flag'] = (df['delivery_status'] == 'Advance shipping').astype(int)
    df['canceled_flag'] = (df['delivery_status'] == 'Shipping canceled').astype(int)
    
    # C. DELIVERY PERFORMANCE CATEGORY
    def categorize_performance(row):
        if row['delivery_status'] == 'Shipping canceled':
            return 'Cancelled'
        elif row['late_delivery_flag'] == 1:
            return 'Late'
        elif row['on_time_flag'] == 1:
            return 'On Time'
        else:
            return 'Early'
            
    df['delivery_performance_category'] = df.apply(categorize_performance, axis=1)
    
    # D. TIME FEATURES
    df['order_year'] = df['order_date'].dt.year
    df['order_month'] = df['order_date'].dt.month
    df['order_quarter'] = df['order_date'].dt.quarter
    df['order_week'] = df['order_date'].dt.isocalendar().week.astype(int)
    df['order_day'] = df['order_date'].dt.day
    df['order_weekday'] = df['order_date'].dt.day_name()
    df['order_hour'] = df['order_date'].dt.hour
    df['order_year_month'] = df['order_date'].dt.strftime('%Y-%m')
    df['is_weekend'] = (df['order_date'].dt.dayofweek >= 5).astype(int)
    
    # E. ORDER & FINANCIAL FEATURES
    df['order_quantity'] = df['order_item_quantity']
    df['quantity_per_order'] = df['order_item_quantity']
    df['order_value'] = df['sales']
    df['order_profit'] = df['order_profit_per_order']
    df['discount_rate'] = df['order_item_discount_rate']
    df['profit_margin'] = np.where(df['sales'] > 0, df['order_profit_per_order'] / df['sales'], 0.0)
    df['revenue_per_unit'] = np.where(df['order_item_quantity'] > 0, df['sales'] / df['order_item_quantity'], 0.0)
    
    # F. OPERATIONAL RISK FLAGS
    df['shipping_delay_risk'] = df['late_delivery_flag']
    df['high_delay_flag'] = (df['shipping_delay_days'] >= 2).astype(int)
    df['critical_delay_flag'] = (df['shipping_delay_days'] >= 3).astype(int)
    
    # G. CATEGORY & REGION OPERATIONAL AGGREGATES
    cat_delay = df.groupby('category_id')['late_delivery_flag'].transform('mean')
    df['category_delay_rate'] = cat_delay
    
    cat_vol = df.groupby('category_id')['order_item_id'].transform('count')
    df['category_volume'] = cat_vol
    
    region_delay = df.groupby('order_region')['late_delivery_flag'].transform('mean')
    df['region_delay_rate'] = region_delay
    
    sm_delay = df.groupby('shipping_mode')['late_delivery_flag'].transform('mean')
    df['shipping_mode_risk'] = sm_delay
    
    # Composite Risk Index
    df['composite_risk_score'] = (df['shipping_mode_risk'] * 0.4) + (df['region_delay_rate'] * 0.3) + (df['category_delay_rate'] * 0.3)
    
    # Save processed analytics dataset
    output_path = os.path.join(analytics_dir, "dataco_featured.csv")
    df.to_csv(output_path, index=False)
    print(f"Featured dataset saved to {output_path} with shape {df.shape}")
    
    # Update cleaned dataset
    df.to_csv(cleaned_path, index=False)
    print(f"Updated {cleaned_path} with engineered features")

if __name__ == "__main__":
    run_feature_engineering()
