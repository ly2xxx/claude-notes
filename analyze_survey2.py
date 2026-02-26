import csv
import json
import statistics

rows = []
with open(r'h:\code\yl\claude-notes\excel-report-workspace\test-data\employee_survey.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

total = len(rows)
print(f"Total rows: {total}")

# Missing values
for col in ['EmployeeID','Department','YearsAtCompany','SatisfactionRating','Salary','LastReviewScore','Comments']:
    missing = sum(1 for r in rows if r[col].strip() == '')
    print(f"Missing {col}: {missing} ({round(missing/total*100,1)}%)")

# Satisfaction ratings
sat_vals = [int(float(r['SatisfactionRating'])) for r in rows if r['SatisfactionRating'].strip()]
print(f"\nSatisfaction: n={len(sat_vals)}, min={min(sat_vals)}, max={max(sat_vals)}, mean={round(statistics.mean(sat_vals),2)}, median={statistics.median(sat_vals)}, stdev={round(statistics.stdev(sat_vals),2)}")
# Distribution
for v in range(1,6):
    c = sat_vals.count(v)
    print(f"  Rating {v}: {c} ({round(c/len(sat_vals)*100,1)}%)")

# Salary
sal_vals = [float(r['Salary']) for r in rows if r['Salary'].strip()]
print(f"\nSalary: n={len(sal_vals)}, min={min(sal_vals)}, max={max(sal_vals)}, mean={round(statistics.mean(sal_vals),2)}, median={statistics.median(sal_vals)}, stdev={round(statistics.stdev(sal_vals),2)}")
sal_sorted = sorted(sal_vals)
Q1 = sal_sorted[len(sal_sorted)//4]
Q3 = sal_sorted[3*len(sal_sorted)//4]
IQR = Q3 - Q1
lb = Q1 - 1.5*IQR
ub = Q3 + 1.5*IQR
outliers_sal = [v for v in sal_vals if v < lb or v > ub]
print(f"  Q1={Q1}, Q3={Q3}, IQR={IQR}, bounds=[{lb},{ub}], outliers={sorted(outliers_sal)}")

# LastReviewScore
rev_vals = [float(r['LastReviewScore']) for r in rows if r['LastReviewScore'].strip()]
print(f"\nLastReviewScore: n={len(rev_vals)}, min={min(rev_vals)}, max={max(rev_vals)}, mean={round(statistics.mean(rev_vals),2)}, median={statistics.median(rev_vals)}, stdev={round(statistics.stdev(rev_vals),2)}")

# YearsAtCompany
yr_vals = [int(r['YearsAtCompany']) for r in rows if r['YearsAtCompany'].strip()]
print(f"\nYearsAtCompany: n={len(yr_vals)}, min={min(yr_vals)}, max={max(yr_vals)}, mean={round(statistics.mean(yr_vals),2)}, median={statistics.median(yr_vals)}, stdev={round(statistics.stdev(yr_vals),2)}")

# Department breakdown
depts = {}
for r in rows:
    d = r['Department']
    if d not in depts:
        depts[d] = {'count':0, 'sats':[], 'sals':[], 'revs':[], 'yrs':[]}
    depts[d]['count'] += 1
    if r['SatisfactionRating'].strip():
        depts[d]['sats'].append(int(float(r['SatisfactionRating'])))
    if r['Salary'].strip():
        depts[d]['sals'].append(float(r['Salary']))
    if r['LastReviewScore'].strip():
        depts[d]['revs'].append(float(r['LastReviewScore']))
    if r['YearsAtCompany'].strip():
        depts[d]['yrs'].append(int(r['YearsAtCompany']))

print("\nDepartment stats:")
for d in sorted(depts.keys()):
    info = depts[d]
    avg_sat = round(statistics.mean(info['sats']),2) if info['sats'] else 'N/A'
    avg_sal = round(statistics.mean(info['sals']),2) if info['sals'] else 'N/A'
    avg_rev = round(statistics.mean(info['revs']),2) if info['revs'] else 'N/A'
    avg_yr = round(statistics.mean(info['yrs']),2) if info['yrs'] else 'N/A'
    print(f"  {d}: count={info['count']}, avg_sat={avg_sat}, avg_sal={avg_sal}, avg_rev={avg_rev}, avg_tenure={avg_yr}")

# Comments
comments = [r['Comments'] for r in rows if r['Comments'].strip()]
print(f"\nComments: {len(comments)} provided, {total - len(comments)} missing")
from collections import Counter
cc = Counter(comments)
for c, n in cc.most_common():
    print(f"  '{c}': {n}")

# Low satisfaction by dept
low_sat_rows = [r for r in rows if r['SatisfactionRating'].strip() and int(float(r['SatisfactionRating'])) == 1]
print(f"\nLow satisfaction (rating=1): {len(low_sat_rows)} employees")
low_depts = Counter(r['Department'] for r in low_sat_rows)
for d, n in low_depts.most_common():
    print(f"  {d}: {n}")

# High salary outliers
print(f"\nSalary outliers (above {ub}):")
for r in rows:
    s = float(r['Salary'])
    if s > ub:
        print(f"  {r['EmployeeID']} ({r['Department']}): ${s:,.0f}, Satisfaction={r['SatisfactionRating'] or 'N/A'}")
