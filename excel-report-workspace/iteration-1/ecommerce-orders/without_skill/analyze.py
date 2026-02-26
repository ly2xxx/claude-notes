import pandas as pd
import json
from datetime import datetime

df = pd.read_csv(r'h:\code\yl\claude-notes\excel-report-workspace\test-data\ecommerce_orders.csv')

# Parse dates
df['Date'] = pd.to_datetime(df['Date'])

results = {}

# === Basic Overview ===
results['total_orders'] = len(df)
results['date_range_start'] = df['Date'].min().strftime('%Y-%m-%d')
results['date_range_end'] = df['Date'].max().strftime('%Y-%m-%d')
results['unique_customers'] = df['Customer'].nunique()
results['total_revenue'] = round(df['Amount'].sum(), 2)
results['total_quantity'] = int(df['Quantity'].sum())
results['avg_order_value'] = round(df['Amount'].mean(), 2)
results['median_order_value'] = round(df['Amount'].median(), 2)
results['min_order_value'] = round(df['Amount'].min(), 2)
results['max_order_value'] = round(df['Amount'].max(), 2)

# === Status Breakdown ===
status_counts = df['Status'].value_counts().to_dict()
results['status_counts'] = {k: int(v) for k, v in status_counts.items()}
status_revenue = df.groupby('Status')['Amount'].sum().round(2).to_dict()
results['status_revenue'] = status_revenue

# === Category Analysis ===
cat_stats = df.groupby('Category').agg(
    orders=('OrderID', 'count'),
    total_revenue=('Amount', 'sum'),
    avg_order=('Amount', 'mean'),
    total_qty=('Quantity', 'sum')
).round(2)
cat_stats = cat_stats.sort_values('total_revenue', ascending=False)
results['category_stats'] = cat_stats.reset_index().to_dict('records')

# === Region Analysis ===
reg_stats = df.groupby('Region').agg(
    orders=('OrderID', 'count'),
    total_revenue=('Amount', 'sum'),
    avg_order=('Amount', 'mean'),
    unique_customers=('Customer', 'nunique')
).round(2)
reg_stats = reg_stats.sort_values('total_revenue', ascending=False)
results['region_stats'] = reg_stats.reset_index().to_dict('records')

# === Monthly Trends ===
df['Month'] = df['Date'].dt.to_period('M')
monthly = df.groupby('Month').agg(
    orders=('OrderID', 'count'),
    revenue=('Amount', 'sum'),
    avg_order=('Amount', 'mean')
).round(2)
monthly.index = monthly.index.astype(str)
results['monthly_stats'] = monthly.reset_index().rename(columns={'Month': 'month'}).to_dict('records')

# === Top Customers ===
top_cust = df.groupby('Customer').agg(
    orders=('OrderID', 'count'),
    total_spent=('Amount', 'sum')
).round(2).sort_values('total_spent', ascending=False).head(10)
results['top_customers'] = top_cust.reset_index().to_dict('records')

# === Region x Category Revenue ===
region_cat = df.pivot_table(index='Region', columns='Category', values='Amount', aggfunc='sum', fill_value=0).round(2)
results['region_category_revenue'] = region_cat.reset_index().to_dict('records')

# === Category x Status Counts ===
cat_status = df.pivot_table(index='Category', columns='Status', values='OrderID', aggfunc='count', fill_value=0)
results['category_status'] = cat_status.reset_index().to_dict('records')

# === Cancellation & Return Rates ===
cancelled = df[df['Status'] == 'Cancelled']
returned = df[df['Status'] == 'Returned']
results['cancellation_rate'] = round(len(cancelled) / len(df) * 100, 1)
results['return_rate'] = round(len(returned) / len(df) * 100, 1)
results['cancelled_revenue_lost'] = round(cancelled['Amount'].sum(), 2)
results['returned_revenue_lost'] = round(returned['Amount'].sum(), 2)

# === Quarterly ===
df['Quarter'] = df['Date'].dt.to_period('Q')
quarterly = df.groupby('Quarter').agg(
    orders=('OrderID', 'count'),
    revenue=('Amount', 'sum'),
    avg_order=('Amount', 'mean')
).round(2)
quarterly.index = quarterly.index.astype(str)
results['quarterly_stats'] = quarterly.reset_index().rename(columns={'Quarter': 'quarter'}).to_dict('records')

# === Repeat Customers ===
cust_order_counts = df.groupby('Customer')['OrderID'].count()
results['single_order_customers'] = int((cust_order_counts == 1).sum())
results['repeat_customers'] = int((cust_order_counts > 1).sum())
results['max_orders_by_customer'] = int(cust_order_counts.max())

# Print as JSON
print(json.dumps(results, default=str))
