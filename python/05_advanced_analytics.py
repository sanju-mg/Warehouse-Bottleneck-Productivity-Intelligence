"""
05_advanced_analytics.py
Warehouse Bottleneck & Productivity Intelligence
Advanced Analytics, Anomaly Detection & Forecasting Script
"""

import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import Ridge
from scipy import stats

def run_advanced_analytics():
    input_path = "data/processed/analytics/dataco_featured.csv"
    analytics_dir = "data/processed/analytics"
    os.makedirs(analytics_dir, exist_ok=True)
    
    print("Loading featured dataset for advanced analytics...")
    df = pd.read_csv(input_path)
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # 1. ANOMALY DETECTION USING ISOLATION FOREST
    print("\n--- 1. Shipping Delay Anomaly Detection (Isolation Forest) ---")
    features_iso = ['actual_shipping_days', 'scheduled_shipping_days', 'shipping_delay_days', 'sales', 'order_item_quantity']
    iso_data = df[features_iso].fillna(0)
    
    iso_model = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
    df['anomaly_isolation_forest'] = iso_model.fit_predict(iso_data)
    anomaly_count = (df['anomaly_isolation_forest'] == -1).sum()
    print(f"Detected {anomaly_count:,} anomalous shipments ({anomaly_count/len(df)*100:.2f}%) using Isolation Forest.")
    
    # 2. Z-SCORE ANOMALY DETECTION ON SHIPPING DELAY
    print("\n--- 2. Z-score Anomaly Detection on Shipping Variance ---")
    df['delay_zscore'] = stats.zscore(df['shipping_delay_days'])
    df['anomaly_zscore'] = (df['delay_zscore'].abs() > 3).astype(int)
    zscore_anomalies = df['anomaly_zscore'].sum()
    print(f"Detected {zscore_anomalies:,} extreme shipping delay outliers (|Z| > 3).")
    
    # 3. ROLLING LATE-DELIVERY RATE & TREND
    print("\n--- 3. Monthly & 3-Month Rolling Late-Delivery Trend ---")
    monthly_summary = df.groupby('order_year_month').agg(
        total_orders=('order_id', 'nunique'),
        order_item_volume=('order_item_id', 'count'),
        late_item_volume=('late_delivery_flag', 'sum'),
        late_delivery_rate=('late_delivery_flag', 'mean'),
        avg_shipping_variance=('shipping_delay_days', 'mean'),
        total_sales=('sales', 'sum')
    ).reset_index()
    
    monthly_summary['rolling_3m_late_rate'] = monthly_summary['late_delivery_rate'].rolling(window=3, min_periods=1).mean()
    monthly_summary['rolling_3m_item_volume'] = monthly_summary['order_item_volume'].rolling(window=3, min_periods=1).mean()
    
    print("Latest 5 Months Rolling Summary:")
    print(monthly_summary[['order_year_month', 'order_item_volume', 'late_delivery_rate', 'rolling_3m_late_rate', 'avg_shipping_variance']].tail(5))
    
    # 4. TIME SERIES FORECASTING OF ORDER VOLUME & LATE DELIVERIES
    print("\n--- 4. Time Series Volume & Late Delivery Forecasting ---")
    monthly_summary['time_index'] = np.arange(len(monthly_summary))
    
    X_train = monthly_summary[['time_index']]
    y_vol = monthly_summary['order_item_volume']
    y_late = monthly_summary['late_item_volume']
    
    model_vol = Ridge(alpha=1.0)
    model_vol.fit(X_train, y_vol)
    
    model_late = Ridge(alpha=1.0)
    model_late.fit(X_train, y_late)
    
    future_indices = np.arange(len(monthly_summary), len(monthly_summary) + 6)
    future_X = pd.DataFrame({'time_index': future_indices})
    
    future_vol_pred = model_vol.predict(future_X)
    future_late_pred = model_late.predict(future_X)
    
    last_ym = pd.to_datetime(monthly_summary['order_year_month'].iloc[-1] + "-01")
    future_dates = [ (last_ym + pd.DateOffset(months=i)).strftime('%Y-%m') for i in range(1, 7) ]
    
    forecast_df = pd.DataFrame({
        'forecast_year_month': future_dates,
        'predicted_order_item_volume': np.round(future_vol_pred).astype(int),
        'predicted_late_item_volume': np.round(future_late_pred).astype(int),
        'predicted_late_delivery_rate': np.round((future_late_pred / future_vol_pred) * 100, 2)
    })
    
    print("\nNext 6-Month Operations Forecast:")
    print(forecast_df)
    
    # 5. EXPORT ANALYTICS & FORECAST RESULTS
    anomalies_export_path = os.path.join(analytics_dir, "dataco_anomalies.csv")
    forecast_export_path = os.path.join(analytics_dir, "dataco_forecasts.csv")
    monthly_summary_path = os.path.join(analytics_dir, "dataco_monthly_analytics.csv")
    
    df[df['anomaly_isolation_forest'] == -1].to_csv(anomalies_export_path, index=False)
    forecast_df.to_csv(forecast_export_path, index=False)
    monthly_summary.to_csv(monthly_summary_path, index=False)
    
    print(f"\nSaved anomaly records ({anomaly_count:,}) to {anomalies_export_path}")
    print(f"Saved forecast results to {forecast_export_path}")
    print(f"Saved monthly analytics to {monthly_summary_path}")

if __name__ == "__main__":
    run_advanced_analytics()
