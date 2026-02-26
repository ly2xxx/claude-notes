import pandas as pd
import json
import sys

df = pd.read_csv(r'h:\code\yl\claude-notes\excel-report-workspace\test-data\employee_survey.csv')

results = {}

# Basic info
results['shape'] = list(df.shape)
results['columns'] = list(df.columns)
results['dtypes'] = {col: str(dtype) for col, dtype in df.dtypes.items()}

# Missing values
results['missing_counts'] = df.isnull().sum().to_dict()
results['missing_pct'] = (df.isnull().sum() / len(df) * 100).round(1).to_dict()

# Numeric stats
results['numeric_describe'] = df.describe().to_dict()

# Department breakdown
results['dept_counts'] = df['Department'].value_counts().to_dict()

# Satisfaction by department
sat_by_dept = df.groupby('Department')['SatisfactionRating'].agg(['mean', 'median', 'std', 'count']).round(2)
results['satisfaction_by_dept'] = sat_by_dept.to_dict()

# Salary by department
sal_by_dept = df.groupby('Department')['Salary'].agg(['mean', 'median', 'min', 'max', 'std']).round(2)
results['salary_by_dept'] = sal_by_dept.to_dict()

# Review score by department
rev_by_dept = df.groupby('Department')['LastReviewScore'].agg(['mean', 'median', 'count']).round(2)
results['review_by_dept'] = rev_by_dept.to_dict()

# Comment analysis
comments = df['Comments'].dropna()
results['comment_counts'] = comments.value_counts().to_dict()
results['total_comments'] = len(comments)
results['no_comments'] = int(df['Comments'].isnull().sum())

# Comments by department
comment_dept = df[df['Comments'].notna()].groupby(['Department', 'Comments']).size().reset_index(name='count')
results['comments_by_dept'] = comment_dept.to_dict(orient='records')

# Satisfaction distribution
results['satisfaction_dist'] = df['SatisfactionRating'].value_counts().sort_index().to_dict()

# Low satisfaction employees (rating 1)
low_sat = df[df['SatisfactionRating'] == 1][['EmployeeID', 'Department', 'YearsAtCompany', 'Salary', 'LastReviewScore', 'Comments']]
results['low_satisfaction'] = low_sat.to_dict(orient='records')

# Salary outliers (IQR method)
Q1 = df['Salary'].quantile(0.25)
Q3 = df['Salary'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['Salary'] < lower_bound) | (df['Salary'] > upper_bound)]
results['salary_outliers'] = outliers[['EmployeeID', 'Department', 'Salary', 'YearsAtCompany']].to_dict(orient='records')
results['salary_iqr'] = {'Q1': Q1, 'Q3': Q3, 'IQR': IQR, 'lower_bound': lower_bound, 'upper_bound': upper_bound}

# Correlation between satisfaction and salary
valid = df.dropna(subset=['SatisfactionRating', 'Salary'])
results['corr_satisfaction_salary'] = round(valid['SatisfactionRating'].corr(valid['Salary']), 4)

# Correlation between satisfaction and review score
valid2 = df.dropna(subset=['SatisfactionRating', 'LastReviewScore'])
results['corr_satisfaction_review'] = round(valid2['SatisfactionRating'].corr(valid2['LastReviewScore']), 4)

# Correlation between salary and review score
valid3 = df.dropna(subset=['Salary', 'LastReviewScore'])
results['corr_salary_review'] = round(valid3['Salary'].corr(valid3['LastReviewScore']), 4)

# Years at company vs satisfaction
tenure_sat = df.groupby(pd.cut(df['YearsAtCompany'], bins=[0, 5, 10, 15, 20, 30], right=True))['SatisfactionRating'].agg(['mean', 'count']).round(2)
results['tenure_satisfaction'] = {str(k): v for k, v in tenure_sat.to_dict(orient='index').items()}

# Employees with missing review scores
missing_review = df[df['LastReviewScore'].isnull()][['EmployeeID', 'Department', 'YearsAtCompany']]
results['missing_review_employees'] = missing_review.to_dict(orient='records')
results['missing_review_by_dept'] = df[df['LastReviewScore'].isnull()]['Department'].value_counts().to_dict()

# Overall satisfaction
results['overall_satisfaction_mean'] = round(df['SatisfactionRating'].mean(), 2)
results['overall_satisfaction_median'] = float(df['SatisfactionRating'].median()) if not pd.isna(df['SatisfactionRating'].median()) else None
results['overall_salary_mean'] = round(df['Salary'].mean(), 2)
results['overall_salary_median'] = float(df['Salary'].median())

# Percentage of employees with low satisfaction (1 or 2)
low_or_very_low = len(df[df['SatisfactionRating'].isin([1, 2])])
rated = len(df[df['SatisfactionRating'].notna()])
results['pct_low_satisfaction'] = round(low_or_very_low / rated * 100, 1)
results['rated_count'] = rated
results['total_count'] = len(df)

# High performer / low satisfaction paradox
paradox = df[(df['LastReviewScore'] >= 4.0) & (df['SatisfactionRating'] <= 2)]
results['high_perf_low_sat'] = paradox[['EmployeeID', 'Department', 'LastReviewScore', 'SatisfactionRating', 'Salary', 'Comments']].to_dict(orient='records')

output_path = r'h:\code\yl\claude-notes\excel-report-workspace\iteration-1\employee-survey\without_skill\outputs\analysis_results.json'
import os
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("Analysis complete. Results saved.")
print(f"Records: {len(df)}")
print(f"Departments: {list(df['Department'].unique())}")
