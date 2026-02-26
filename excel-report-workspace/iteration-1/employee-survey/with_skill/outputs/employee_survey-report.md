# Data Report: employee_survey.csv

## Executive Summary

This dataset contains employee survey results for 150 employees across five departments (Engineering, HR, Marketing, Operations, and Sales). The data captures satisfaction ratings, salaries, performance review scores, tenure, and open-ended comments. The most notable finding is a significant data completeness issue: **22.7% of performance review scores and 54.0% of employee comments are missing**, which may undermine the reliability of conclusions drawn from those fields. Additionally, 4 salary outliers were detected (up to $247,729 against a median of $70,981), and 15.7% of respondents who provided a rating gave the lowest possible satisfaction score of 1.

## Data Overview

| Property  | Value |
|-----------|-------|
| Rows      | 150   |
| Columns   | 7     |
| File type | CSV   |

### Column Descriptions

| Column              | Type        | Non-Null Count | Description |
|---------------------|-------------|----------------|-------------|
| EmployeeID          | Categorical | 150 (100%)     | Unique employee identifier (format: EMP-NNN) |
| Department          | Categorical | 150 (100%)     | Employee's department (5 unique values) |
| YearsAtCompany      | Numeric     | 150 (100%)     | Tenure in years (integer, 0-25 range) |
| SatisfactionRating  | Numeric     | 127 (84.7%)    | Employee satisfaction score on a 1-5 scale |
| Salary              | Numeric     | 150 (100%)     | Annual salary in USD |
| LastReviewScore     | Numeric     | 116 (77.3%)    | Most recent performance review score (2.0-5.0 scale) |
| Comments            | Text        | 69 (46.0%)     | Free-text survey comment |

## Key Findings

### Satisfaction Ratings

- The **average satisfaction rating is 3.21 out of 5** (median: 3.0, standard deviation: 1.41), indicating moderate satisfaction with high variability.
- The distribution is relatively spread across all five levels:
  - Rating 5 (highest): 32 employees (25.2%)
  - Rating 4: 25 employees (19.7%)
  - Rating 3: 28 employees (22.0%)
  - Rating 2: 22 employees (17.3%)
  - Rating 1 (lowest): 20 employees (15.7%)
- **20 employees (15.7% of respondents) gave the lowest rating of 1** -- a significant pocket of dissatisfaction that warrants attention.
- Satisfaction is fairly consistent across departments, ranging from 3.08 (Operations) to 3.32 (Sales).

### Salary

- Salaries range from **$33,911 to $247,729**, with a mean of **$74,935** and a median of **$70,981**.
- Standard deviation is $27,336, indicating moderate salary dispersion.
- **4 salary outliers** were detected (above the upper bound of $116,523 based on 1.5x IQR):
  - **EMP-033** (Engineering): **$247,729** -- satisfaction rating of 4
  - **EMP-077** (Sales): **$241,488** -- satisfaction rating of 2, with 0 years tenure (new hire with very high salary)
  - **EMP-038** (HR): **$138,268** -- satisfaction rating not provided
  - **EMP-058** (HR): **$125,168** -- satisfaction rating of 3
- EMP-077 is particularly noteworthy: a brand-new employee (0 years) with a $241,488 salary and a satisfaction rating of only 2.

### Performance Review Scores

- Review scores range from **2.0 to 5.0**, with a mean of **3.50** and median of **3.55**.
- Standard deviation is 0.85, indicating moderate spread.
- **34 employees (22.7%) have no review score on file** -- this exceeds the 20% threshold and represents a data quality concern.

### Tenure

- Average tenure is **12.85 years** (median: 13.0 years), with a range of 0 to 25 years.
- Standard deviation is 7.05 years, indicating a wide distribution of experience levels.
- Operations has the highest average tenure (13.62 years) while Sales has the lowest (11.62 years).

### Department Breakdown

| Department   | Employees | Avg Satisfaction | Avg Salary  | Avg Review Score | Avg Tenure (yrs) |
|--------------|-----------|------------------|-------------|------------------|-------------------|
| Sales        | 29        | 3.32             | $80,137     | 3.56             | 11.62             |
| Marketing    | 29        | 3.26             | $74,941     | 3.30             | 13.17             |
| HR           | 35        | 3.23             | $75,902     | 3.46             | 13.26             |
| Engineering  | 28        | 3.16             | $73,851     | 3.62             | 12.46             |
| Operations   | 29        | 3.08             | $69,605     | 3.60             | 13.62             |

- **Operations has both the lowest average satisfaction (3.08) and the lowest average salary ($69,605)** -- a potential correlation worth investigating.
- **Sales has the highest satisfaction (3.32) and the highest average salary ($80,137)**.
- **Engineering has the highest average review score (3.62)** but below-average satisfaction (3.16), suggesting strong performers who may not feel adequately recognized or compensated.

### Employee Comments

- Only **69 out of 150 employees (46.0%) left a comment**, meaning over half declined to respond to the open-ended question.
- All 69 comments fall into exactly **3 categories** (no free-form responses were captured):
  - **"More PTO please"**: 27 mentions (39.1% of comments) -- the most common theme
  - **"Need better tools"**: 22 mentions (31.9% of comments)
  - **"Great place to work"**: 20 mentions (29.0% of comments)
- The fact that all comments are one of three exact strings suggests these may have been **pre-defined response options** rather than true open-ended feedback. This is important context when presenting these results.

### Low Satisfaction Deep Dive

The 20 employees who rated satisfaction as 1 (lowest) are distributed as follows:

| Department   | Count |
|--------------|-------|
| HR           | 5     |
| Sales        | 5     |
| Engineering  | 4     |
| Operations   | 3     |
| Marketing    | 3     |

- HR and Sales each have the highest count of highly dissatisfied employees (5 each).
- Given that HR has the largest headcount (35), its proportion of low-satisfaction employees (5/35 = 14.3%) is roughly in line with the overall rate. However, Sales has only 29 employees making its rate (5/29 = 17.2%) higher than average.

### Data Quality Issues

- **SatisfactionRating**: 23 missing values (15.3%) -- below the 20% concern threshold, but still notable for a key metric.
- **LastReviewScore**: 34 missing values (22.7%) -- **exceeds the 20% threshold**. Over one-fifth of employees have no review score recorded.
- **Comments**: 81 missing values (54.0%) -- more than half of employees did not provide a comment.
- **No duplicate rows** were found in the dataset.
- EmployeeID, Department, YearsAtCompany, and Salary are 100% complete.

## Recommendations

- **Investigate the 4 salary outliers** -- particularly EMP-077 (Sales, $241,488 salary, 0 years tenure, satisfaction of 2) and EMP-033 (Engineering, $247,729). Verify these figures are accurate and not data entry errors. If accurate, understand why EMP-077 is dissatisfied despite the high compensation.
- **Address the missing review scores** -- 22.7% of employees lack a LastReviewScore. This gap could indicate inconsistent performance review processes. Ensure all employees receive timely reviews before the next survey cycle.
- **Dig deeper into Operations department satisfaction** -- Operations has the lowest average satisfaction (3.08) and the lowest average salary ($69,605). Consider whether compensation adjustments or other interventions are warranted.
- **Revisit the comments collection method** -- the fact that all 69 comments are one of exactly three strings suggests the survey used a limited set of predefined options rather than open text. For richer qualitative feedback, consider adding a true free-text field in the next survey.
- **Take the "More PTO please" signal seriously** -- this was the most frequent comment (27 mentions, 39.1% of all comments). Combined with moderate overall satisfaction scores, PTO policy may be a meaningful lever for improving employee sentiment.
- **Recognize Engineering performance** -- Engineering has the highest average review score (3.62) but below-average satisfaction (3.16) and salaries ($73,851). This combination of high performance and lower satisfaction is a retention risk.
- **Follow up with the 20 lowest-rated employees** -- 15.7% of respondents rated satisfaction as 1. Targeted conversations or stay interviews could help identify specific pain points and prevent attrition.
- **Improve survey response rates for Comments** -- with a 54.0% missing rate, leadership is only hearing from less than half the workforce. Consider making the comment field required or incentivizing completion.
