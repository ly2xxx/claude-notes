# Data Report: ecommerce_orders.csv

## Executive Summary

This dataset contains 200 online orders placed throughout 2025, spanning five product categories across four geographic regions. Total revenue across all orders is $20,751.65, with an average order value of $103.76. The most notable finding is the presence of three high-value outlier orders exceeding $1,000 each (up to $1,304.64), which significantly inflate the mean and standard deviation of the Amount column.

## Data Overview

| Property  | Value |
|-----------|-------|
| Rows      | 200   |
| Columns   | 8     |
| File type | CSV   |
| Date range| January 3, 2025 to December 27, 2025 |
| Total revenue | $20,751.65 |

### Column Descriptions

| Column   | Type        | Non-Null Count | Description |
|----------|-------------|----------------|-------------|
| OrderID  | String      | 200            | Unique order identifier (format: ORD-XXXX, sequential from 0001 to 0200) |
| Date     | Date/String | 200            | Order date in YYYY-MM-DD format, spanning all of 2025 |
| Customer | String      | 200            | Anonymized customer identifier (format: Customer_XXX) |
| Region   | Categorical | 200            | Geographic region: North, South, East, or West |
| Category | Categorical | 200            | Product category: Sports, Home & Garden, Clothing, Books, or Electronics |
| Amount   | Float       | 200            | Order dollar amount, ranging from $5.00 to $1,304.64 |
| Quantity | Integer     | 200            | Number of items in the order, ranging from 1 to 8 |
| Status   | Categorical | 200            | Order status: Delivered, Shipped, Processing, Cancelled, or Returned |

## Key Findings

### Data Quality
- **No missing values**: All 200 rows are complete across all 8 columns -- data quality is excellent.
- **No duplicate rows** and no duplicate OrderIDs -- each record is unique.
- **Six orders have a suspiciously round Amount of exactly $5.00**, which could indicate placeholder values, minimum-charge orders, or gift cards. These appear across multiple categories (Sports, Clothing, Home & Garden, Books) and statuses.

### Revenue and Order Amounts
- **Mean order value**: $103.76, **Median**: $89.81 -- the median being lower than the mean indicates a right-skewed distribution pulled up by high-value outliers.
- **Standard deviation**: $143.63 -- very high relative to the mean, driven almost entirely by three outlier orders.
- **Three outlier orders** (beyond 1.5x IQR upper fence of $197.14):
  - ORD-0142: $1,304.64 (Electronics, Returned)
  - ORD-0015: $1,257.53 (Electronics, Delivered)
  - ORD-0088: $1,101.84 (Books, Cancelled)
- Without these three outliers, the typical order range is $5.00 to about $177.72.

### Category Breakdown
- **Sports** has the most orders (45, 22.5%) but the lowest average order value ($81.60).
- **Electronics** has the fewest orders (31, 15.5%) but the highest average order value ($166.73), significantly inflated by the two outlier orders in this category.
- **Books**: 39 orders, mean $114.09, also boosted by one $1,101.84 outlier.
- **Clothing**: 41 orders, mean $83.49 -- the most consistent category with no outliers.
- **Home & Garden**: 44 orders, mean $91.77 -- fairly evenly distributed.

### Regional Distribution
- **South** is the most active region with 61 orders (30.5%), generating $6,387.45 in total revenue.
- **East** follows with 58 orders (29.0%) and $6,100.41 in total revenue.
- **North**: 41 orders (20.5%), highest mean order value at $113.32.
- **West**: 40 orders (20.0%), lowest mean order value at $90.44.
- South and East together account for nearly 60% of all orders.

### Order Status
- **Delivered**: 79 orders (39.5%) -- the most common status, indicating healthy fulfillment.
- **Shipped**: 65 orders (32.5%) -- a large portion still in transit.
- **Processing**: 24 orders (12.0%) -- orders not yet shipped.
- **Cancelled**: 21 orders (10.5%) -- a notable cancellation rate worth monitoring.
- **Returned**: 11 orders (5.5%) -- the returned orders have the highest mean amount ($201.71), largely due to the $1,304.64 outlier (ORD-0142).

### Customer Patterns
- **184 unique customers** out of 200 orders -- most customers placed only one order.
- Only 16 repeat orders observed (from customers with 2 orders each), indicating low repeat purchase rates.

### Seasonal Trends
- **November** was the busiest month with 25 orders, likely reflecting holiday season demand.
- **January** had the fewest orders (12), consistent with a post-holiday slowdown.
- Order volume is generally higher in Q4 (October-December: 62 orders) compared to Q1 (January-March: 46 orders).

## Recommendations

- **Verify the three high-value outlier orders** ($1,101.84 to $1,304.64) -- these are 10-12x the median order value and may represent bulk purchases, pricing errors, or legitimate large orders. Notably, one was Returned and another Cancelled.
- **Investigate the six orders at exactly $5.00** -- determine if these are minimum charges, test orders, or gift card purchases, and whether they should be included in revenue analysis.
- **Address the 10.5% cancellation rate** -- with 21 cancelled orders, it would be worth analyzing cancellation reasons by category and region to identify friction points.
- **Monitor the Returned category more closely** -- while only 5.5% of orders, the high average return amount ($201.71) suggests expensive items are returned more often. Electronics appear overrepresented in returns.
- **Focus retention efforts on repeat purchases** -- with 92% of customers placing only one order, there is significant opportunity to improve customer lifetime value through loyalty programs or follow-up marketing.
- **Capitalize on Q4 demand** -- November's 25 orders represent the seasonal peak. Consider inventory planning and promotional campaigns to maximize the holiday sales window.
- **Expand North and West market share** -- these regions account for only 40.5% of orders combined. Targeted campaigns may help balance regional distribution.
