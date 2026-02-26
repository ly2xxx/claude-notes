import csv
import os
from collections import defaultdict

# Read CSV
rows = []
with open(r'h:\code\yl\claude-notes\excel-report-workspace\test-data\ecommerce_orders.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['Amount'] = float(row['Amount'])
        row['Quantity'] = int(row['Quantity'])
        rows.append(row)

total_orders = len(rows)
amounts = [r['Amount'] for r in rows]
quantities = [r['Quantity'] for r in rows]
total_revenue = sum(amounts)
total_quantity = sum(quantities)
avg_order = total_revenue / total_orders
min_amount = min(amounts)
max_amount = max(amounts)

# Median
sorted_amounts = sorted(amounts)
n = len(sorted_amounts)
if n % 2 == 0:
    median_amount = (sorted_amounts[n//2 - 1] + sorted_amounts[n//2]) / 2
else:
    median_amount = sorted_amounts[n//2]

# Date range
dates = sorted([r['Date'] for r in rows])
date_start = dates[0]
date_end = dates[-1]

# Unique customers
customers = set(r['Customer'] for r in rows)
unique_customers = len(customers)

# Status breakdown
status_counts = defaultdict(int)
status_revenue = defaultdict(float)
status_qty = defaultdict(int)
for r in rows:
    status_counts[r['Status']] += 1
    status_revenue[r['Status']] += r['Amount']
    status_qty[r['Status']] += r['Quantity']

# Category analysis
cat_orders = defaultdict(int)
cat_revenue = defaultdict(float)
cat_qty = defaultdict(int)
for r in rows:
    cat_orders[r['Category']] += 1
    cat_revenue[r['Category']] += r['Amount']
    cat_qty[r['Category']] += r['Quantity']

categories = sorted(cat_revenue.keys(), key=lambda c: cat_revenue[c], reverse=True)

# Region analysis
reg_orders = defaultdict(int)
reg_revenue = defaultdict(float)
reg_customers = defaultdict(set)
for r in rows:
    reg_orders[r['Region']] += 1
    reg_revenue[r['Region']] += r['Amount']
    reg_customers[r['Region']].add(r['Customer'])

regions = sorted(reg_revenue.keys(), key=lambda c: reg_revenue[c], reverse=True)

# Monthly trends
monthly_orders = defaultdict(int)
monthly_revenue = defaultdict(float)
for r in rows:
    month = r['Date'][:7]  # YYYY-MM
    monthly_orders[month] += 1
    monthly_revenue[month] += r['Amount']

months_sorted = sorted(monthly_orders.keys())
month_names = {
    '01': 'January', '02': 'February', '03': 'March', '04': 'April',
    '05': 'May', '06': 'June', '07': 'July', '08': 'August',
    '09': 'September', '10': 'October', '11': 'November', '12': 'December'
}

# Quarterly
quarterly_orders = defaultdict(int)
quarterly_revenue = defaultdict(float)
for r in rows:
    m = int(r['Date'][5:7])
    q = (m - 1) // 3 + 1
    y = r['Date'][:4]
    qkey = f"{y}-Q{q}"
    quarterly_orders[qkey] += 1
    quarterly_revenue[qkey] += r['Amount']

quarters_sorted = sorted(quarterly_orders.keys())

# Top 10 customers
cust_orders = defaultdict(int)
cust_spent = defaultdict(float)
for r in rows:
    cust_orders[r['Customer']] += 1
    cust_spent[r['Customer']] += r['Amount']

top_customers = sorted(cust_spent.keys(), key=lambda c: cust_spent[c], reverse=True)[:10]

# Repeat customers
single_order = sum(1 for c in cust_orders if cust_orders[c] == 1)
repeat = sum(1 for c in cust_orders if cust_orders[c] > 1)
max_orders_per_cust = max(cust_orders.values())

# Region x Category revenue
region_cat_rev = defaultdict(lambda: defaultdict(float))
for r in rows:
    region_cat_rev[r['Region']][r['Category']] += r['Amount']

all_cats = sorted(set(r['Category'] for r in rows))

# Category x Status
cat_status_count = defaultdict(lambda: defaultdict(int))
for r in rows:
    cat_status_count[r['Category']][r['Status']] += 1

all_statuses = sorted(status_counts.keys())

# Cancellation and return rates
cancelled_count = status_counts.get('Cancelled', 0)
returned_count = status_counts.get('Returned', 0)
cancel_rate = cancelled_count / total_orders * 100
return_rate = returned_count / total_orders * 100
cancelled_rev = status_revenue.get('Cancelled', 0)
returned_rev = status_revenue.get('Returned', 0)

# Highest single order
max_order_row = max(rows, key=lambda r: r['Amount'])

# Category by region cancellation
region_cancel = defaultdict(int)
region_total = defaultdict(int)
for r in rows:
    region_total[r['Region']] += 1
    if r['Status'] == 'Cancelled':
        region_cancel[r['Region']] += 1

# Build the report
lines = []
lines.append("# E-Commerce Orders Summary Report")
lines.append("")
lines.append(f"**Report Generated From:** `ecommerce_orders.csv`")
lines.append(f"**Date Range:** {date_start} to {date_end}")
lines.append(f"**Total Records Analyzed:** {total_orders}")
lines.append("")

lines.append("---")
lines.append("")
lines.append("## 1. High-Level Overview")
lines.append("")
lines.append("| Metric | Value |")
lines.append("|---|---|")
lines.append(f"| Total Orders | {total_orders} |")
lines.append(f"| Unique Customers | {unique_customers} |")
lines.append(f"| Total Revenue | ${total_revenue:,.2f} |")
lines.append(f"| Total Items Sold | {total_quantity:,} |")
lines.append(f"| Average Order Value | ${avg_order:,.2f} |")
lines.append(f"| Median Order Value | ${median_amount:,.2f} |")
lines.append(f"| Min Order Value | ${min_amount:,.2f} |")
lines.append(f"| Max Order Value | ${max_amount:,.2f} |")
lines.append(f"| Avg Items per Order | {total_quantity / total_orders:.1f} |")
lines.append("")

lines.append("The single largest order was **{oid}** ({cust}, {cat}) for **${amt:,.2f}**.".format(
    oid=max_order_row['OrderID'], cust=max_order_row['Customer'],
    cat=max_order_row['Category'], amt=max_order_row['Amount']
))
lines.append("")

lines.append("---")
lines.append("")
lines.append("## 2. Order Status Breakdown")
lines.append("")
lines.append("| Status | Orders | % of Total | Revenue | Avg Order Value |")
lines.append("|---|---|---|---|---|")
for s in sorted(status_counts.keys(), key=lambda x: status_counts[x], reverse=True):
    pct = status_counts[s] / total_orders * 100
    avg = status_revenue[s] / status_counts[s] if status_counts[s] > 0 else 0
    lines.append(f"| {s} | {status_counts[s]} | {pct:.1f}% | ${status_revenue[s]:,.2f} | ${avg:,.2f} |")
lines.append("")

lines.append(f"**Cancellation Rate:** {cancel_rate:.1f}% ({cancelled_count} orders, ${cancelled_rev:,.2f} in lost revenue)")
lines.append("")
lines.append(f"**Return Rate:** {return_rate:.1f}% ({returned_count} orders, ${returned_rev:,.2f} in returned value)")
lines.append("")

lines.append("---")
lines.append("")
lines.append("## 3. Revenue by Product Category")
lines.append("")
lines.append("| Category | Orders | Revenue | % of Revenue | Avg Order | Total Qty |")
lines.append("|---|---|---|---|---|---|")
for c in categories:
    pct = cat_revenue[c] / total_revenue * 100
    avg = cat_revenue[c] / cat_orders[c]
    lines.append(f"| {c} | {cat_orders[c]} | ${cat_revenue[c]:,.2f} | {pct:.1f}% | ${avg:,.2f} | {cat_qty[c]} |")
lines.append("")

lines.append("**Key Observations:**")
lines.append("")
top_cat = categories[0]
bot_cat = categories[-1]
lines.append(f"- **{top_cat}** leads in total revenue with ${cat_revenue[top_cat]:,.2f} across {cat_orders[top_cat]} orders.")
lines.append(f"- **{bot_cat}** has the lowest revenue share at ${cat_revenue[bot_cat]:,.2f}.")

# Find highest avg order category
highest_avg_cat = max(categories, key=lambda c: cat_revenue[c] / cat_orders[c])
lines.append(f"- **{highest_avg_cat}** has the highest average order value at ${cat_revenue[highest_avg_cat] / cat_orders[highest_avg_cat]:,.2f}.")
lines.append("")

lines.append("---")
lines.append("")
lines.append("## 4. Revenue by Region")
lines.append("")
lines.append("| Region | Orders | Revenue | % of Revenue | Avg Order | Unique Customers |")
lines.append("|---|---|---|---|---|---|")
for reg in regions:
    pct = reg_revenue[reg] / total_revenue * 100
    avg = reg_revenue[reg] / reg_orders[reg]
    lines.append(f"| {reg} | {reg_orders[reg]} | ${reg_revenue[reg]:,.2f} | {pct:.1f}% | ${avg:,.2f} | {len(reg_customers[reg])} |")
lines.append("")

lines.append("**Key Observations:**")
lines.append("")
top_reg = regions[0]
bot_reg = regions[-1]
lines.append(f"- **{top_reg}** is the top-performing region with ${reg_revenue[top_reg]:,.2f} in revenue.")
lines.append(f"- **{bot_reg}** trails with ${reg_revenue[bot_reg]:,.2f} in revenue.")
for reg in regions:
    cr = region_cancel.get(reg, 0) / region_total[reg] * 100
    if cr > cancel_rate + 2:
        lines.append(f"- **{reg}** has an above-average cancellation rate of {cr:.1f}%.")
lines.append("")

lines.append("---")
lines.append("")
lines.append("## 5. Region-Category Revenue Matrix")
lines.append("")
header = "| Region | " + " | ".join(all_cats) + " | Total |"
sep = "|---|" + "|".join(["---"] * len(all_cats)) + "|---|"
lines.append(header)
lines.append(sep)
for reg in sorted(region_cat_rev.keys()):
    vals = []
    total = 0
    for cat in all_cats:
        v = region_cat_rev[reg][cat]
        vals.append(f"${v:,.2f}")
        total += v
    lines.append(f"| {reg} | " + " | ".join(vals) + f" | ${total:,.2f} |")
lines.append("")

lines.append("---")
lines.append("")
lines.append("## 6. Monthly Trends")
lines.append("")
lines.append("| Month | Orders | Revenue | Avg Order Value |")
lines.append("|---|---|---|---|")
for m in months_sorted:
    mname = month_names[m[5:7]] + " " + m[:4]
    avg = monthly_revenue[m] / monthly_orders[m]
    lines.append(f"| {mname} | {monthly_orders[m]} | ${monthly_revenue[m]:,.2f} | ${avg:,.2f} |")
lines.append("")

# Find peak and trough
peak_month = max(months_sorted, key=lambda m: monthly_revenue[m])
trough_month = min(months_sorted, key=lambda m: monthly_revenue[m])
peak_name = month_names[peak_month[5:7]] + " " + peak_month[:4]
trough_name = month_names[trough_month[5:7]] + " " + trough_month[:4]

lines.append("**Key Observations:**")
lines.append("")
lines.append(f"- **Peak revenue month:** {peak_name} with ${monthly_revenue[peak_month]:,.2f} across {monthly_orders[peak_month]} orders.")
lines.append(f"- **Lowest revenue month:** {trough_name} with ${monthly_revenue[trough_month]:,.2f} across {monthly_orders[trough_month]} orders.")
lines.append("")

lines.append("---")
lines.append("")
lines.append("## 7. Quarterly Performance")
lines.append("")
lines.append("| Quarter | Orders | Revenue | Avg Order Value |")
lines.append("|---|---|---|---|")
for q in quarters_sorted:
    avg = quarterly_revenue[q] / quarterly_orders[q]
    lines.append(f"| {q} | {quarterly_orders[q]} | ${quarterly_revenue[q]:,.2f} | ${avg:,.2f} |")
lines.append("")

# QoQ growth
if len(quarters_sorted) >= 2:
    lines.append("**Quarter-over-Quarter Revenue Growth:**")
    lines.append("")
    for i in range(1, len(quarters_sorted)):
        prev = quarterly_revenue[quarters_sorted[i-1]]
        curr = quarterly_revenue[quarters_sorted[i]]
        growth = (curr - prev) / prev * 100
        direction = "up" if growth > 0 else "down"
        lines.append(f"- {quarters_sorted[i-1]} -> {quarters_sorted[i]}: {direction} {abs(growth):.1f}%")
    lines.append("")

lines.append("---")
lines.append("")
lines.append("## 8. Category x Status Distribution")
lines.append("")
header = "| Category | " + " | ".join(all_statuses) + " | Total |"
sep = "|---|" + "|".join(["---"] * len(all_statuses)) + "|---|"
lines.append(header)
lines.append(sep)
for cat in sorted(cat_status_count.keys()):
    vals = []
    total = 0
    for s in all_statuses:
        v = cat_status_count[cat].get(s, 0)
        vals.append(str(v))
        total += v
    lines.append(f"| {cat} | " + " | ".join(vals) + f" | {total} |")
lines.append("")

lines.append("---")
lines.append("")
lines.append("## 9. Top 10 Customers by Total Spend")
lines.append("")
lines.append("| Rank | Customer | Orders | Total Spent | Avg per Order |")
lines.append("|---|---|---|---|---|")
for i, c in enumerate(top_customers, 1):
    avg = cust_spent[c] / cust_orders[c]
    lines.append(f"| {i} | {c} | {cust_orders[c]} | ${cust_spent[c]:,.2f} | ${avg:,.2f} |")
lines.append("")

lines.append("---")
lines.append("")
lines.append("## 10. Customer Loyalty")
lines.append("")
lines.append("| Metric | Value |")
lines.append("|---|---|")
lines.append(f"| Single-Order Customers | {single_order} ({single_order/unique_customers*100:.1f}%) |")
lines.append(f"| Repeat Customers (2+ orders) | {repeat} ({repeat/unique_customers*100:.1f}%) |")
lines.append(f"| Max Orders by a Single Customer | {max_orders_per_cust} |")
lines.append(f"| Revenue per Customer (avg) | ${total_revenue/unique_customers:,.2f} |")
lines.append("")

lines.append("---")
lines.append("")
lines.append("## 11. Key Takeaways")
lines.append("")
lines.append(f"1. **Overall Health:** The dataset covers {total_orders} orders generating ${total_revenue:,.2f} in revenue across {unique_customers} unique customers over the period {date_start} to {date_end}.")
lines.append("")

delivered_shipped = status_counts.get('Delivered', 0) + status_counts.get('Shipped', 0)
ds_pct = delivered_shipped / total_orders * 100
lines.append(f"2. **Fulfillment:** {ds_pct:.0f}% of orders are either Delivered or Shipped, indicating strong fulfillment performance.")
lines.append("")

lines.append(f"3. **Cancellations & Returns:** Combined cancellation and return rate is {cancel_rate + return_rate:.1f}%. Cancellations account for ${cancelled_rev:,.2f} and returns for ${returned_rev:,.2f} in lost/at-risk revenue.")
lines.append("")

lines.append(f"4. **Top Category:** {top_cat} leads revenue at ${cat_revenue[top_cat]:,.2f} ({cat_revenue[top_cat]/total_revenue*100:.1f}% of total).")
lines.append("")

lines.append(f"5. **Top Region:** {top_reg} leads with ${reg_revenue[top_reg]:,.2f} ({reg_revenue[top_reg]/total_revenue*100:.1f}% of total revenue).")
lines.append("")

lines.append(f"6. **Seasonality:** Revenue peaked in {peak_name} (${monthly_revenue[peak_month]:,.2f}) and was lowest in {trough_name} (${monthly_revenue[trough_month]:,.2f}).")
lines.append("")

lines.append(f"7. **Customer Base:** {single_order/unique_customers*100:.0f}% of customers placed only one order, suggesting opportunity for retention campaigns to drive repeat purchases.")
lines.append("")

# Write the report
output_dir = r'h:\code\yl\claude-notes\excel-report-workspace\iteration-1\ecommerce-orders\without_skill\outputs'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'ecommerce_orders-report.md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print(f"Report written to {output_path}")
print(f"Total lines: {len(lines)}")
