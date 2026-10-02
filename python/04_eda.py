"""
04_eda.py
Warehouse Bottleneck & Productivity Intelligence
Exploratory Data Analysis Chart Generation Script
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#eeeeee'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['figure.titlesize'] = 14
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

def generate_eda_charts():
    input_path = "data/processed/analytics/dataco_featured.csv"
    eda_dir = "data/processed/eda"
    os.makedirs(eda_dir, exist_ok=True)
    
    print("Loading featured dataset for EDA chart generation...")
    df = pd.read_csv(input_path)
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    late_color = '#e63946'
    ontime_color = '#2a9d8f'
    neutral_color = '#457b9d'
    
    # 1. Order Volume Trend
    plt.figure(figsize=(12, 5))
    monthly_vol = df.groupby('order_year_month')['order_item_id'].count()
    plt.plot(monthly_vol.index, monthly_vol.values, marker='o', color=neutral_color, linewidth=2, markersize=4)
    plt.title('Monthly Order Item Volume Trend (2015 - 2018)', fontweight='bold', pad=15)
    plt.xlabel('Year-Month')
    plt.ylabel('Order-Item Volume')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '01_order_volume_trend.png'), dpi=300)
    plt.close()
    
    # 2. Overall Late Delivery Rate
    plt.figure(figsize=(6, 6))
    late_counts = df['late_delivery_flag'].value_counts()
    labels = ['Late Delivery (54.83%)', 'On Time / Early / Canceled (45.17%)']
    colors = [late_color, ontime_color]
    plt.pie(late_counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops=dict(width=0.4, edgecolor='w'))
    plt.title('Overall Fulfillment SLA Performance', fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '02_late_delivery_rate.png'), dpi=300)
    plt.close()
    
    # 3. Shipping Variance Distribution
    plt.figure(figsize=(9, 5))
    sns.histplot(df['shipping_delay_days'], bins=range(-5, 6), kde=False, color=neutral_color, edgecolor='white')
    plt.axvline(0, color=late_color, linestyle='--', label='Scheduled SLA Target (0 Days Variance)')
    plt.title('Distribution of Shipping Delay Days (Actual vs Scheduled)', fontweight='bold', pad=15)
    plt.xlabel('Shipping Variance (Actual - Scheduled Days)')
    plt.ylabel('Order-Item Count')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '03_shipping_variance_distribution.png'), dpi=300)
    plt.close()
    
    # 4. Actual vs Scheduled Shipping Time
    plt.figure(figsize=(9, 5))
    sm_times = df.groupby('shipping_mode')[['scheduled_shipping_days', 'actual_shipping_days']].mean().reset_index()
    sm_times_melted = pd.melt(sm_times, id_vars=['shipping_mode'], value_vars=['scheduled_shipping_days', 'actual_shipping_days'],
                              var_name='Time Metric', value_name='Days')
    sm_times_melted['Time Metric'] = sm_times_melted['Time Metric'].replace({
        'scheduled_shipping_days': 'Scheduled Shipping Days',
        'actual_shipping_days': 'Actual Shipping Days'
    })
    sns.barplot(data=sm_times_melted, x='shipping_mode', y='Days', hue='Time Metric', palette=[ontime_color, late_color])
    plt.title('Scheduled vs Actual Shipping Days by Shipping Mode', fontweight='bold', pad=15)
    plt.xlabel('Shipping Mode')
    plt.ylabel('Average Days')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '04_actual_vs_scheduled_shipping_time.png'), dpi=300)
    plt.close()
    
    # 5. Shipping Mode Performance
    plt.figure(figsize=(9, 5))
    sm_late = df.groupby('shipping_mode')['late_delivery_flag'].mean().reset_index()
    sm_late['late_pct'] = sm_late['late_delivery_flag'] * 100
    sm_late = sm_late.sort_values('late_pct', ascending=False)
    ax = sns.barplot(data=sm_late, x='shipping_mode', y='late_pct', hue='shipping_mode', palette='Reds_r', legend=False)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='bold')
    plt.title('Late Delivery Rate by Shipping Mode', fontweight='bold', pad=15)
    plt.xlabel('Shipping Mode')
    plt.ylabel('Late Delivery Rate (%)')
    plt.ylim(0, 110)
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '05_shipping_mode_performance.png'), dpi=300)
    plt.close()
    
    # 6. Region Performance
    plt.figure(figsize=(10, 6))
    reg_perf = df.groupby('order_region').agg(
        late_rate=('late_delivery_flag', 'mean'),
        vol=('order_item_id', 'count')
    ).reset_index()
    reg_perf['late_pct'] = reg_perf['late_rate'] * 100
    reg_perf = reg_perf.sort_values('late_pct', ascending=False).head(10)
    sns.barplot(data=reg_perf, y='order_region', x='late_pct', hue='order_region', palette='Oranges_r', legend=False)
    plt.title('Top 10 Regions by Late Delivery Rate (%)', fontweight='bold', pad=15)
    plt.xlabel('Late Delivery Rate (%)')
    plt.ylabel('Order Region')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '06_region_performance.png'), dpi=300)
    plt.close()
    
    # 7. Country Performance
    plt.figure(figsize=(10, 6))
    cntry_perf = df.groupby('order_country').agg(
        late_rate=('late_delivery_flag', 'mean'),
        vol=('order_item_id', 'count')
    ).reset_index()
    cntry_perf = cntry_perf[cntry_perf['vol'] >= 500].sort_values('late_rate', ascending=False).head(10)
    cntry_perf['late_pct'] = cntry_perf['late_rate'] * 100
    sns.barplot(data=cntry_perf, y='order_country', x='late_pct', hue='order_country', palette='YlOrRd_r', legend=False)
    plt.title('Top 10 Problematic Destination Countries (Vol >= 500)', fontweight='bold', pad=15)
    plt.xlabel('Late Delivery Rate (%)')
    plt.ylabel('Order Country')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '07_country_performance.png'), dpi=300)
    plt.close()
    
    # 8. Product Category Performance
    plt.figure(figsize=(10, 6))
    cat_perf = df.groupby('category_name').agg(
        late_rate=('late_delivery_flag', 'mean'),
        vol=('order_item_id', 'count')
    ).reset_index()
    cat_perf = cat_perf[cat_perf['vol'] >= 300].sort_values('late_rate', ascending=False).head(10)
    cat_perf['late_pct'] = cat_perf['late_rate'] * 100
    sns.barplot(data=cat_perf, y='category_name', x='late_pct', hue='category_name', palette='Purples_r', legend=False)
    plt.title('Top 10 Product Categories by Late Delivery Rate (Vol >= 300)', fontweight='bold', pad=15)
    plt.xlabel('Late Delivery Rate (%)')
    plt.ylabel('Category Name')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '08_product_category_performance.png'), dpi=300)
    plt.close()
    
    # 9. Department Performance
    plt.figure(figsize=(10, 5))
    dept_perf = df.groupby('department_name').agg(
        late_rate=('late_delivery_flag', 'mean'),
        vol=('order_item_id', 'count')
    ).reset_index()
    dept_perf['late_pct'] = dept_perf['late_rate'] * 100
    dept_perf = dept_perf.sort_values('late_pct', ascending=False)
    sns.barplot(data=dept_perf, x='department_name', y='late_pct', hue='department_name', palette='Blues_r', legend=False)
    plt.title('Late Delivery Rate across Departments', fontweight='bold', pad=15)
    plt.xlabel('Department Name')
    plt.ylabel('Late Delivery Rate (%)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '09_department_performance.png'), dpi=300)
    plt.close()
    
    # 10. Monthly Late-Delivery Trend
    plt.figure(figsize=(12, 5))
    monthly_late = df.groupby('order_year_month')['late_delivery_flag'].mean() * 100
    plt.plot(monthly_late.index, monthly_late.values, marker='s', color=late_color, linewidth=2, markersize=4)
    plt.axhline(monthly_late.mean(), color='black', linestyle=':', label=f'Average ({monthly_late.mean():.1f}%)')
    plt.title('Monthly Late Delivery Rate Trend (%)', fontweight='bold', pad=15)
    plt.xlabel('Year-Month')
    plt.ylabel('Late Delivery Rate (%)')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '10_monthly_late_delivery_trend.png'), dpi=300)
    plt.close()
    
    # 11. Day-of-Week Performance
    plt.figure(figsize=(9, 5))
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_df = df.groupby('order_weekday')['late_delivery_flag'].mean().reindex(day_order).reset_index()
    dow_df['late_pct'] = dow_df['late_delivery_flag'] * 100
    sns.barplot(data=dow_df, x='order_weekday', y='late_pct', hue='order_weekday', palette='crest', legend=False)
    plt.title('Late Delivery Rate by Day of Week', fontweight='bold', pad=15)
    plt.xlabel('Day of Week')
    plt.ylabel('Late Delivery Rate (%)')
    plt.ylim(0, 70)
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '11_day_of_week_performance.png'), dpi=300)
    plt.close()
    
    # 12. Customer Segment Performance
    plt.figure(figsize=(8, 5))
    seg_df = (df.groupby('customer_segment')['late_delivery_flag'].mean() * 100).reset_index()
    seg_df.columns = ['customer_segment', 'late_pct']
    sns.barplot(data=seg_df, x='customer_segment', y='late_pct', hue='customer_segment', palette='viridis', legend=False)
    plt.title('Late Delivery Rate by Customer Segment', fontweight='bold', pad=15)
    plt.xlabel('Customer Segment')
    plt.ylabel('Late Delivery Rate (%)')
    plt.ylim(0, 70)
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '12_customer_segment_analysis.png'), dpi=300)
    plt.close()
    
    # 13. Quantity vs Shipping Delay
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x='order_item_quantity', y='shipping_delay_days', hue='order_item_quantity', palette='coolwarm', legend=False)
    plt.title('Shipping Delay Days by Order Line Quantity', fontweight='bold', pad=15)
    plt.xlabel('Order Item Quantity')
    plt.ylabel('Shipping Delay Days')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '13_quantity_vs_shipping_delay.png'), dpi=300)
    plt.close()
    
    # 14. Sales vs Shipping Delay
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=df, x='shipping_delay_days', y='sales', hue='shipping_delay_days', palette='Blues', legend=False)
    plt.title('Sales Value Distribution by Shipping Delay Days', fontweight='bold', pad=15)
    plt.xlabel('Shipping Delay Days')
    plt.ylabel('Sales ($)')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '14_sales_vs_shipping_delay.png'), dpi=300)
    plt.close()
    
    # 15. Profit vs Shipping Delay
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=df, x='shipping_delay_days', y='order_profit_per_order', hue='shipping_delay_days', palette='Greens', legend=False)
    plt.title('Order Profit Distribution by Shipping Delay Days', fontweight='bold', pad=15)
    plt.xlabel('Shipping Delay Days')
    plt.ylabel('Order Profit ($)')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '15_profit_vs_shipping_delay.png'), dpi=300)
    plt.close()
    
    # 16. Delivery Status Breakdown
    plt.figure(figsize=(8, 5))
    ds_df = df['delivery_status'].value_counts().reset_index()
    ds_df.columns = ['delivery_status', 'count']
    sns.barplot(data=ds_df, x='delivery_status', y='count', hue='delivery_status', palette='Spectral', legend=False)
    plt.title('Distribution of Delivery Status Types', fontweight='bold', pad=15)
    plt.xlabel('Delivery Status')
    plt.ylabel('Order Item Count')
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '16_delivery_status_distribution.png'), dpi=300)
    plt.close()
    
    # 17. Top Delayed Regions Matrix
    plt.figure(figsize=(10, 6))
    reg_matrix = df.groupby('order_region').agg(
        vol=('order_item_id', 'count'),
        late_pct=('late_delivery_flag', lambda x: x.mean() * 100)
    ).reset_index()
    sns.scatterplot(data=reg_matrix, x='vol', y='late_pct', size='vol', sizes=(50, 400), hue='late_pct', palette='Reds', legend=False)
    for i, row in reg_matrix.iterrows():
        plt.text(row['vol'] + 200, row['late_pct'], row['order_region'], fontsize=8)
    plt.title('Region Risk Matrix: Order Volume vs Late Delivery Rate (%)', fontweight='bold', pad=15)
    plt.xlabel('Total Order Volume (Order Items)')
    plt.ylabel('Late Delivery Rate (%)')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '17_top_delayed_regions_matrix.png'), dpi=300)
    plt.close()
    
    # 18. Top Delayed Categories
    plt.figure(figsize=(10, 6))
    cat_matrix = df.groupby('category_name').agg(
        vol=('order_item_id', 'count'),
        late_pct=('late_delivery_flag', lambda x: x.mean() * 100)
    ).reset_index()
    cat_matrix = cat_matrix[cat_matrix['vol'] >= 1000]
    sns.scatterplot(data=cat_matrix, x='vol', y='late_pct', size='vol', sizes=(50, 400), hue='late_pct', palette='Wistia', legend=False)
    for i, row in cat_matrix.iterrows():
        plt.text(row['vol'] + 200, row['late_pct'], row['category_name'], fontsize=8)
    plt.title('Category Bottleneck Matrix (Volume >= 1000)', fontweight='bold', pad=15)
    plt.xlabel('Order Item Volume')
    plt.ylabel('Late Delivery Rate (%)')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '18_top_delayed_categories.png'), dpi=300)
    plt.close()
    
    # 19. Shipping Mode Bottleneck Ranking
    plt.figure(figsize=(9, 5))
    sm_gap = df.groupby('shipping_mode')['shipping_delay_days'].mean().reset_index().sort_values('shipping_delay_days', ascending=False)
    sns.barplot(data=sm_gap, x='shipping_mode', y='shipping_delay_days', hue='shipping_mode', palette='flare', legend=False)
    plt.title('Shipping Mode SLA Gap Ranking (Average Delay Days)', fontweight='bold', pad=15)
    plt.xlabel('Shipping Mode')
    plt.ylabel('Average Shipping Delay (Days)')
    plt.axhline(0, color='black', linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '19_shipping_mode_bottleneck_ranking.png'), dpi=300)
    plt.close()
    
    # 20. Composite Operational Risk Distribution
    plt.figure(figsize=(9, 5))
    sns.histplot(df['composite_risk_score'], bins=30, kde=True, color=late_color)
    plt.title('Composite Operational Risk Index Distribution', fontweight='bold', pad=15)
    plt.xlabel('Composite Risk Index (0.0 to 1.0)')
    plt.ylabel('Order-Item Frequency')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, '20_operational_risk_distribution.png'), dpi=300)
    plt.close()
    
    print(f"Successfully generated 20 EDA charts in {eda_dir}")

if __name__ == "__main__":
    generate_eda_charts()
