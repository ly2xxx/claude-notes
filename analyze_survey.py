import pandas as pd
import json
import numpy as np

df = pd.read_csv(r'h:\code\yl\claude-notes\excel-report-workspace\test-data\employee_survey.csv')

results = {}

# Shape
results['rows'] = int(df.shape[0])
results['cols'] = int(df.shape[1])
results['columns'] = list(df.columns)

# Column types
results['dtypes'] = {col: str(df[col].dtype) for col in df.columns}

# Missing values
missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
results['missing'] = {col: {'count': int(missing[col]), 'pct': float(missing_pct[col])} for col in df.columns}

# Numeric columns summary
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
results['numeric_summary'] = {}
for col in numeric_cols:
    s = df[col].dropna()
    Q1 = float(s.quantile(0.25))
    Q3 = float(s.quantile(0.75))
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = s[(s < lower_bound) | (s > upper_bound)]
    results['numeric_summary'][col] = {
        'min': float(s.min()),
        'max': float(s.max()),
        'mean': round(float(s.mean()), 2),
        'median': float(s.median()),
        'std': round(float(s.std()), 2),
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'outlier_count': int(len(outliers)),
        'outlier_values': sorted(outliers.tolist())
    }

# Categorical columns summary
cat_cols = df.select_dtypes(include=['object']).columns.tolist()
results['categorical_summary'] = {}
for col in cat_cols:
    vc = df[col].value_counts()
    results['categorical_summary'][col] = {
        'unique': int(df[col].nunique()),
        'top_values': {str(k): int(v) for k, v in vc.head(5).items()}
    }

# Department breakdown
dept_stats = df.groupby('Department').agg(
    count=('EmployeeID', 'count'),
    avg_satisfaction=('SatisfactionRating', 'mean'),
    avg_salary=('Salary', 'mean'),
    avg_review=('LastReviewScore', 'mean'),
    avg_tenure=('YearsAtCompany', 'mean')
).round(2)
results['dept_stats'] = dept_stats.to_dict('index')

# Satisfaction distribution
sat_dist = df['SatisfactionRating'].dropna().value_counts().sort_index()
results['satisfaction_distribution'] = {str(int(k)): int(v) for k, v in sat_dist.items()}

# Comments analysis
comments = df['Comments'].dropna()
comment_counts = comments.value_counts()
results['comment_summary'] = {str(k): int(v) for k, v in comment_counts.items()}
results['comments_total'] = int(len(comments))
results['comments_missing'] = int(df['Comments'].isnull().sum())

# Duplicates
results['duplicates'] = int(df.duplicated().sum())

# Correlation between key numeric fields
valid = df[['SatisfactionRating', 'Salary', 'LastReviewScore', 'YearsAtCompany']].dropna()
if len(valid) > 2:
    corr = valid.corr().round(3)
    results['correlation'] = corr.to_dict()

# Low satisfaction employees (rating 1)
low_sat = df[df['SatisfactionRating'] == 1]
results['low_satisfaction_count'] = int(len(low_sat))
results['low_satisfaction_depts'] = {str(k): int(v) for k, v in low_sat['Department'].value_counts().items()}

print(json.dumps(results, indent=2))
