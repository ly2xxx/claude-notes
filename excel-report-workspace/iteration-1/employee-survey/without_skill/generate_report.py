import pandas as pd
import os

df = pd.read_csv(r'h:\code\yl\claude-notes\excel-report-workspace\test-data\employee_survey.csv')

lines = []
def w(s=""):
    lines.append(s)

# ============================================================
# HEADER
# ============================================================
w("# Employee Survey Analysis Report")
w()
w("## Executive Summary")
w()
w(f"This report analyzes survey responses from **{len(df)} employees** across **{df['Department'].nunique()} departments** "
  f"({', '.join(sorted(df['Department'].unique()))}). "
  f"The data covers employee satisfaction ratings, salary information, manager review scores, and open-ended comments.")
w()

# ============================================================
# DATA QUALITY
# ============================================================
w("---")
w()
w("## 1. Data Quality Assessment")
w()
w("### Missing Values")
w()
w("| Column | Missing Count | Missing % | Impact |")
w("|--------|--------------|-----------|--------|")
missing = df.isnull().sum()
for col in df.columns:
    cnt = int(missing[col])
    pct = round(cnt / len(df) * 100, 1)
    if cnt > 0:
        if col == 'SatisfactionRating':
            impact = "HIGH - core survey metric"
        elif col == 'LastReviewScore':
            impact = "HIGH - performance data gap"
        elif col == 'Comments':
            impact = "LOW - optional field"
        else:
            impact = "MEDIUM"
        w(f"| {col} | {cnt} | {pct}% | {impact} |")
    else:
        w(f"| {col} | {cnt} | {pct}% | None |")
w()

# Missing satisfaction by dept
sat_missing_dept = df[df['SatisfactionRating'].isnull()]['Department'].value_counts()
w("**Satisfaction rating is missing for these departments:**")
w()
for dept, cnt in sat_missing_dept.items():
    dept_total = len(df[df['Department'] == dept])
    w(f"- {dept}: {cnt} of {dept_total} employees ({round(cnt/dept_total*100, 1)}%)")
w()

# Missing review score by dept
rev_missing_dept = df[df['LastReviewScore'].isnull()]['Department'].value_counts()
w("**Review score is missing for these departments:**")
w()
for dept, cnt in rev_missing_dept.items():
    dept_total = len(df[df['Department'] == dept])
    w(f"- {dept}: {cnt} of {dept_total} employees ({round(cnt/dept_total*100, 1)}%)")
w()

# Salary outliers
Q1 = df['Salary'].quantile(0.25)
Q3 = df['Salary'].quantile(0.75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR
lower_bound = Q1 - 1.5 * IQR
outliers = df[(df['Salary'] < lower_bound) | (df['Salary'] > upper_bound)]
w("### Salary Outliers")
w()
w(f"Using the IQR method (Q1={Q1:,.0f}, Q3={Q3:,.0f}, IQR={IQR:,.0f}), upper bound = {upper_bound:,.0f}:")
w()
if len(outliers) > 0:
    w("| EmployeeID | Department | Salary | Years at Company | Notes |")
    w("|------------|-----------|--------|-----------------|-------|")
    for _, row in outliers.iterrows():
        sal = f"${row['Salary']:,.0f}"
        notes = "Significantly above peers" if row['Salary'] > upper_bound else "Significantly below peers"
        w(f"| {row['EmployeeID']} | {row['Department']} | {sal} | {int(row['YearsAtCompany'])} | {notes} |")
    w()
    w(f"> **FLAG**: {len(outliers)} salary outlier(s) detected. These could indicate data entry errors, executive-level compensation, or pay equity issues that warrant review.")
else:
    w("No salary outliers detected.")
w()

# ============================================================
# OVERALL METRICS
# ============================================================
w("---")
w()
w("## 2. Overall Workforce Metrics")
w()

rated = df['SatisfactionRating'].dropna()
w(f"- **Total Employees**: {len(df)}")
w(f"- **Satisfaction Responses**: {len(rated)} of {len(df)} ({round(len(rated)/len(df)*100, 1)}%)")
w(f"- **Mean Satisfaction**: {rated.mean():.2f} / 5.0")
w(f"- **Median Satisfaction**: {rated.median():.1f} / 5.0")
w(f"- **Mean Salary**: ${df['Salary'].mean():,.0f}")
w(f"- **Median Salary**: ${df['Salary'].median():,.0f}")
reviewed = df['LastReviewScore'].dropna()
w(f"- **Mean Review Score**: {reviewed.mean():.2f} / 5.0")
w(f"- **Average Tenure**: {df['YearsAtCompany'].mean():.1f} years")
w()

# Satisfaction distribution
w("### Satisfaction Rating Distribution")
w()
w("| Rating | Count | % of Respondents | Interpretation |")
w("|--------|-------|-----------------|----------------|")
sat_dist = rated.value_counts().sort_index()
interpretations = {1: "Very Dissatisfied", 2: "Dissatisfied", 3: "Neutral", 4: "Satisfied", 5: "Very Satisfied"}
for rating in [1, 2, 3, 4, 5]:
    cnt = int(sat_dist.get(rating, 0))
    pct = round(cnt / len(rated) * 100, 1)
    w(f"| {rating} | {cnt} | {pct}% | {interpretations[rating]} |")

low_count = int(sat_dist.get(1, 0)) + int(sat_dist.get(2, 0))
low_pct = round(low_count / len(rated) * 100, 1)
high_count = int(sat_dist.get(4, 0)) + int(sat_dist.get(5, 0))
high_pct = round(high_count / len(rated) * 100, 1)
w()
w(f"> **{low_pct}%** of respondents rated satisfaction at 1 or 2 (dissatisfied), while **{high_pct}%** rated 4 or 5 (satisfied).")
w()

# ============================================================
# DEPARTMENT BREAKDOWN
# ============================================================
w("---")
w()
w("## 3. Department-Level Breakdown")
w()

w("### Headcount by Department")
w()
w("| Department | Headcount | % of Total |")
w("|-----------|-----------|------------|")
dept_counts = df['Department'].value_counts().sort_values(ascending=False)
for dept, cnt in dept_counts.items():
    w(f"| {dept} | {cnt} | {round(cnt/len(df)*100, 1)}% |")
w()

w("### Satisfaction by Department")
w()
w("| Department | Mean Satisfaction | Median | Std Dev | Response Rate | Rank |")
w("|-----------|------------------|--------|---------|---------------|------|")
dept_sat = df.groupby('Department')['SatisfactionRating'].agg(['mean', 'median', 'std', 'count'])
dept_totals = df['Department'].value_counts()
dept_sat['response_rate'] = (dept_sat['count'] / dept_totals * 100).round(1)
dept_sat_sorted = dept_sat.sort_values('mean', ascending=False)
for i, (dept, row) in enumerate(dept_sat_sorted.iterrows(), 1):
    w(f"| {dept} | {row['mean']:.2f} | {row['median']:.1f} | {row['std']:.2f} | {row['response_rate']:.0f}% | {i} |")
w()

w("### Salary by Department")
w()
w("| Department | Mean Salary | Median Salary | Min | Max | Spread (Max-Min) |")
w("|-----------|------------|---------------|-----|-----|-----------------|")
dept_sal = df.groupby('Department')['Salary'].agg(['mean', 'median', 'min', 'max'])
dept_sal['spread'] = dept_sal['max'] - dept_sal['min']
dept_sal_sorted = dept_sal.sort_values('mean', ascending=False)
for dept, row in dept_sal_sorted.iterrows():
    w(f"| {dept} | ${row['mean']:,.0f} | ${row['median']:,.0f} | ${row['min']:,.0f} | ${row['max']:,.0f} | ${row['spread']:,.0f} |")
w()

w("### Review Scores by Department")
w()
w("| Department | Mean Review | Median Review | Reviews Available | Missing Reviews |")
w("|-----------|------------|---------------|-------------------|-----------------|")
dept_rev = df.groupby('Department')['LastReviewScore'].agg(['mean', 'median', 'count'])
dept_rev['missing'] = dept_totals - dept_rev['count']
dept_rev_sorted = dept_rev.sort_values('mean', ascending=False)
for dept, row in dept_rev_sorted.iterrows():
    total = int(dept_totals[dept])
    w(f"| {dept} | {row['mean']:.2f} | {row['median']:.1f} | {int(row['count'])} / {total} | {int(row['missing'])} |")
w()

# ============================================================
# COMMENT ANALYSIS
# ============================================================
w("---")
w()
w("## 4. Comment / Feedback Analysis")
w()

comments = df['Comments'].dropna()
total_with_comments = len(comments)
total_without = len(df) - total_with_comments
w(f"- **Employees who left comments**: {total_with_comments} ({round(total_with_comments/len(df)*100, 1)}%)")
w(f"- **Employees with no comment**: {total_without} ({round(total_without/len(df)*100, 1)}%)")
w()

w("### Comment Theme Distribution")
w()
w("| Theme | Count | % of Comments | Sentiment |")
w("|-------|-------|--------------|-----------|")
comment_counts = comments.value_counts()
sentiments = {
    "More PTO please": "Negative / Request",
    "Great place to work": "Positive",
    "Need better tools": "Negative / Request",
}
for theme, cnt in comment_counts.items():
    pct = round(cnt / total_with_comments * 100, 1)
    sentiment = sentiments.get(theme, "Unknown")
    w(f"| {theme} | {cnt} | {pct}% | {sentiment} |")
w()

# Negative vs positive
positive_themes = ["Great place to work"]
negative_themes = ["More PTO please", "Need better tools"]
pos_count = sum(int(comment_counts.get(t, 0)) for t in positive_themes)
neg_count = sum(int(comment_counts.get(t, 0)) for t in negative_themes)
w(f"> Of those who commented, **{round(neg_count/total_with_comments*100, 1)}%** expressed a concern or request, "
  f"while **{round(pos_count/total_with_comments*100, 1)}%** were positive.")
w()

w("### Comments by Department")
w()
w("| Department | More PTO please | Need better tools | Great place to work | Total Comments |")
w("|-----------|----------------|-------------------|--------------------|--------------:|")
for dept in sorted(df['Department'].unique()):
    dept_df = df[df['Department'] == dept]
    dept_comments = dept_df['Comments'].dropna()
    pto = len(dept_comments[dept_comments == "More PTO please"])
    tools = len(dept_comments[dept_comments == "Need better tools"])
    great = len(dept_comments[dept_comments == "Great place to work"])
    total = len(dept_comments)
    w(f"| {dept} | {pto} | {tools} | {great} | {total} |")
w()

# ============================================================
# CORRELATIONS & PATTERNS
# ============================================================
w("---")
w()
w("## 5. Key Correlations and Patterns")
w()

# Satisfaction vs Salary
valid_ss = df.dropna(subset=['SatisfactionRating', 'Salary'])
corr_ss = valid_ss['SatisfactionRating'].corr(valid_ss['Salary'])
w(f"### Satisfaction vs. Salary")
w(f"- Correlation coefficient: **{corr_ss:.4f}**")
if abs(corr_ss) < 0.1:
    w("- Interpretation: Essentially **no linear relationship** between satisfaction and salary.")
elif abs(corr_ss) < 0.3:
    direction = "positive" if corr_ss > 0 else "negative"
    w(f"- Interpretation: **Weak {direction}** relationship between satisfaction and salary.")
elif abs(corr_ss) < 0.5:
    direction = "positive" if corr_ss > 0 else "negative"
    w(f"- Interpretation: **Moderate {direction}** relationship between satisfaction and salary.")
w()

# Satisfaction vs Review
valid_sr = df.dropna(subset=['SatisfactionRating', 'LastReviewScore'])
corr_sr = valid_sr['SatisfactionRating'].corr(valid_sr['LastReviewScore'])
w(f"### Satisfaction vs. Review Score")
w(f"- Correlation coefficient: **{corr_sr:.4f}**")
if abs(corr_sr) < 0.1:
    w("- Interpretation: Essentially **no relationship** between how satisfied employees are and how they perform in reviews.")
elif abs(corr_sr) < 0.3:
    direction = "positive" if corr_sr > 0 else "negative"
    w(f"- Interpretation: **Weak {direction}** relationship.")
w()

# Tenure vs Satisfaction
w("### Satisfaction by Tenure Band")
w()
bins = [0, 5, 10, 15, 20, 30]
labels = ['0-5 yrs', '6-10 yrs', '11-15 yrs', '16-20 yrs', '21+ yrs']
df['TenureBand'] = pd.cut(df['YearsAtCompany'], bins=bins, labels=labels, right=True)
tenure_sat = df.groupby('TenureBand', observed=False)['SatisfactionRating'].agg(['mean', 'median', 'count'])
w("| Tenure Band | Mean Satisfaction | Median | Respondents |")
w("|------------|------------------|--------|-------------|")
for band, row in tenure_sat.iterrows():
    w(f"| {band} | {row['mean']:.2f} | {row['median']:.1f} | {int(row['count'])} |")
w()

# ============================================================
# HIGH-PERFORMER / LOW-SATISFACTION (FLIGHT RISK)
# ============================================================
w("---")
w()
w("## 6. Flight Risk: High Performers with Low Satisfaction")
w()
w("Employees with a review score >= 4.0 but satisfaction rating <= 2 represent a **retention risk** -- "
  "they are valued contributors who may be looking to leave.")
w()

paradox = df[(df['LastReviewScore'] >= 4.0) & (df['SatisfactionRating'] <= 2)]
if len(paradox) > 0:
    w(f"**{len(paradox)} employees** identified:")
    w()
    w("| EmployeeID | Department | Review Score | Satisfaction | Salary | Tenure | Comment |")
    w("|------------|-----------|-------------|-------------|--------|--------|---------|")
    for _, row in paradox.iterrows():
        comment = row['Comments'] if pd.notna(row['Comments']) else "--"
        sal = f"${row['Salary']:,.0f}"
        w(f"| {row['EmployeeID']} | {row['Department']} | {row['LastReviewScore']} | {int(row['SatisfactionRating'])} | {sal} | {int(row['YearsAtCompany'])} yrs | {comment} |")
    w()
    w("> **ACTION NEEDED**: These employees are performing well but are unhappy. Consider targeted retention conversations.")
else:
    w("No high-performer / low-satisfaction employees identified.")
w()

# ============================================================
# LOW SATISFACTION DEEP DIVE
# ============================================================
w("---")
w()
w("## 7. Low Satisfaction Deep Dive (Rating = 1)")
w()
low_sat = df[df['SatisfactionRating'] == 1]
w(f"**{len(low_sat)} employees** gave the lowest possible satisfaction rating:")
w()
w("| EmployeeID | Department | Tenure | Salary | Review Score | Comment |")
w("|------------|-----------|--------|--------|-------------|---------|")
for _, row in low_sat.iterrows():
    review = f"{row['LastReviewScore']}" if pd.notna(row['LastReviewScore']) else "Missing"
    comment = row['Comments'] if pd.notna(row['Comments']) else "--"
    w(f"| {row['EmployeeID']} | {row['Department']} | {int(row['YearsAtCompany'])} yrs | ${row['Salary']:,.0f} | {review} | {comment} |")
w()

low_sat_depts = low_sat['Department'].value_counts()
w("**Distribution by department:**")
w()
for dept, cnt in low_sat_depts.items():
    dept_total_rated = len(df[(df['Department'] == dept) & (df['SatisfactionRating'].notna())])
    w(f"- {dept}: {cnt} employees ({round(cnt/dept_total_rated*100, 1)}% of rated employees in dept)")
w()

# ============================================================
# FLAGS FOR LEADERSHIP
# ============================================================
w("---")
w()
w("## 8. Key Flags and Recommendations for Leadership")
w()

w("### Critical Flags")
w()

# Flag 1: Missing data
sat_missing = int(df['SatisfactionRating'].isnull().sum())
rev_missing = int(df['LastReviewScore'].isnull().sum())
w(f"1. **Significant Data Gaps**: {sat_missing} employees ({round(sat_missing/len(df)*100, 1)}%) have no satisfaction rating, "
  f"and {rev_missing} ({round(rev_missing/len(df)*100, 1)}%) are missing review scores. "
  f"This undermines the reliability of department-level conclusions. "
  f"Investigate whether these are non-responses, new hires, or system issues.")
w()

# Flag 2: Low satisfaction rate
w(f"2. **{low_pct}% Dissatisfaction Rate**: Nearly a third of respondents rated satisfaction at 1 or 2. "
  f"This is a significant proportion and suggests systemic issues, not isolated cases.")
w()

# Flag 3: PTO is top concern
pto_count = int(comment_counts.get("More PTO please", 0))
w(f"3. **PTO Is the Top Concern**: \"{comment_counts.index[0]}\" is the most frequent comment theme "
  f"({pto_count} mentions, {round(pto_count/total_with_comments*100, 1)}% of all comments). "
  f"Consider benchmarking your PTO policy against industry standards.")
w()

# Flag 4: Tooling complaints
tools_count = int(comment_counts.get("Need better tools", 0))
w(f"4. **Tooling Complaints**: {tools_count} employees cited needing better tools. "
  f"This may be impacting both satisfaction and productivity. "
  f"An infrastructure/tooling audit may be warranted, especially in departments with the most complaints.")
w()

# Flag 5: Flight risk
w(f"5. **Retention Risk -- {len(paradox)} High Performers Are Dissatisfied**: "
  f"These employees have strong review scores (>= 4.0) but low satisfaction (<= 2). "
  f"Losing these employees would directly impact team performance. "
  f"Immediate 1:1 conversations recommended.")
w()

# Flag 6: Salary outliers
if len(outliers) > 0:
    w(f"6. **Salary Outliers Detected**: {len(outliers)} employee(s) have salaries significantly outside the normal range. "
      f"Review for data accuracy or equity concerns.")
    w()

# Flag 7: Department specific
worst_dept = dept_sat_sorted.index[-1]
worst_mean = dept_sat_sorted.iloc[-1]['mean']
best_dept = dept_sat_sorted.index[0]
best_mean = dept_sat_sorted.iloc[0]['mean']
w(f"7. **Department Disparity**: {worst_dept} has the lowest mean satisfaction ({worst_mean:.2f}), "
  f"while {best_dept} has the highest ({best_mean:.2f}). "
  f"This {best_mean - worst_mean:.2f}-point gap deserves targeted investigation in the underperforming department.")
w()

w("### Recommendations")
w()
w("1. **Immediate**: Conduct stay interviews with the identified flight-risk employees (high performers with low satisfaction)")
w("2. **Short-term**: Benchmark and review PTO policy against industry peers; this is the single most common employee concern")
w("3. **Short-term**: Conduct a tooling/infrastructure needs assessment, especially in Engineering and Operations")
w("4. **Medium-term**: Investigate and close the data gaps -- ensure 100% survey completion and review score coverage")
w(f"5. **Medium-term**: Deep-dive into {worst_dept} department to understand drivers of low satisfaction")
w("6. **Ongoing**: Establish regular pulse surveys to track satisfaction trends over time, rather than relying on point-in-time snapshots")
w()

w("---")
w()
w("## Appendix: Data Summary Statistics")
w()
w("### Numeric Columns")
w()
desc = df[['YearsAtCompany', 'SatisfactionRating', 'Salary', 'LastReviewScore']].describe().round(2)
w("| Statistic | YearsAtCompany | SatisfactionRating | Salary | LastReviewScore |")
w("|-----------|---------------|-------------------|--------|----------------|")
for stat in desc.index:
    vals = []
    for col in ['YearsAtCompany', 'SatisfactionRating', 'Salary', 'LastReviewScore']:
        v = desc.loc[stat, col]
        if col == 'Salary':
            vals.append(f"${v:,.0f}")
        else:
            vals.append(f"{v:.2f}")
    w(f"| {stat} | {' | '.join(vals)} |")
w()
w("---")
w()
w("*Report generated from employee_survey.csv (150 records). Analysis performed with pandas.*")

# Write report
output_path = r'h:\code\yl\claude-notes\excel-report-workspace\iteration-1\employee-survey\without_skill\outputs\employee_survey-report.md'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"Report written to {output_path}")
print(f"Report length: {len(lines)} lines")
