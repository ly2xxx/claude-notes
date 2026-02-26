# Employee Survey Analysis Report

## Executive Summary

This report analyzes survey responses from **150 employees** across **5 departments** (Engineering, HR, Marketing, Operations, Sales). The data covers employee satisfaction ratings, salary information, manager review scores, and open-ended comments.

---

## 1. Data Quality Assessment

### Missing Values

| Column | Missing Count | Missing % | Impact |
|--------|--------------|-----------|--------|
| EmployeeID | 0 | 0.0% | None |
| Department | 0 | 0.0% | None |
| YearsAtCompany | 0 | 0.0% | None |
| SatisfactionRating | 23 | 15.3% | HIGH - core survey metric |
| Salary | 0 | 0.0% | None |
| LastReviewScore | 34 | 22.7% | HIGH - performance data gap |
| Comments | 81 | 54.0% | LOW - optional field |

**Satisfaction rating is missing for these departments:**

- Marketing: 6 of 29 employees (20.7%)
- Operations: 5 of 29 employees (17.2%)
- HR: 5 of 35 employees (14.3%)
- Sales: 4 of 29 employees (13.8%)
- Engineering: 3 of 28 employees (10.7%)

**Review score is missing for these departments:**

- Sales: 8 of 29 employees (27.6%)
- Operations: 8 of 29 employees (27.6%)
- Marketing: 7 of 29 employees (24.1%)
- Engineering: 6 of 28 employees (21.4%)
- HR: 5 of 35 employees (14.3%)

### Salary Outliers

Using the IQR method (Q1=61,920, Q3=83,504, IQR=21,584), upper bound = 115,880:

| EmployeeID | Department | Salary | Years at Company | Notes |
|------------|-----------|--------|-----------------|-------|
| EMP-033 | Engineering | $247,729 | 14 | Significantly above peers |
| EMP-038 | HR | $138,268 | 18 | Significantly above peers |
| EMP-058 | HR | $125,168 | 11 | Significantly above peers |
| EMP-077 | Sales | $241,488 | 0 | Significantly above peers |

> **FLAG**: 4 salary outlier(s) detected. These could indicate data entry errors, executive-level compensation, or pay equity issues that warrant review.

---

## 2. Overall Workforce Metrics

- **Total Employees**: 150
- **Satisfaction Responses**: 127 of 150 (84.7%)
- **Mean Satisfaction**: 3.21 / 5.0
- **Median Satisfaction**: 3.0 / 5.0
- **Mean Salary**: $74,935
- **Median Salary**: $70,981
- **Mean Review Score**: 3.50 / 5.0
- **Average Tenure**: 12.8 years

### Satisfaction Rating Distribution

| Rating | Count | % of Respondents | Interpretation |
|--------|-------|-----------------|----------------|
| 1 | 20 | 15.7% | Very Dissatisfied |
| 2 | 22 | 17.3% | Dissatisfied |
| 3 | 28 | 22.0% | Neutral |
| 4 | 25 | 19.7% | Satisfied |
| 5 | 32 | 25.2% | Very Satisfied |

> **33.1%** of respondents rated satisfaction at 1 or 2 (dissatisfied), while **44.9%** rated 4 or 5 (satisfied).

---

## 3. Department-Level Breakdown

### Headcount by Department

| Department | Headcount | % of Total |
|-----------|-----------|------------|
| HR | 35 | 23.3% |
| Sales | 29 | 19.3% |
| Marketing | 29 | 19.3% |
| Operations | 29 | 19.3% |
| Engineering | 28 | 18.7% |

### Satisfaction by Department

| Department | Mean Satisfaction | Median | Std Dev | Response Rate | Rank |
|-----------|------------------|--------|---------|---------------|------|
| Sales | 3.32 | 3.0 | 1.63 | 86% | 1 |
| Marketing | 3.26 | 3.0 | 1.29 | 79% | 2 |
| HR | 3.23 | 3.0 | 1.45 | 86% | 3 |
| Engineering | 3.16 | 3.0 | 1.31 | 89% | 4 |
| Operations | 3.08 | 3.0 | 1.41 | 83% | 5 |

### Salary by Department

| Department | Mean Salary | Median Salary | Min | Max | Spread (Max-Min) |
|-----------|------------|---------------|-----|-----|-----------------|
| Sales | $80,137 | $75,926 | $36,385 | $241,488 | $205,103 |
| HR | $75,902 | $71,216 | $33,911 | $138,268 | $104,357 |
| Marketing | $74,941 | $74,782 | $34,678 | $112,048 | $77,370 |
| Engineering | $73,851 | $69,598 | $34,473 | $247,729 | $213,256 |
| Operations | $69,605 | $67,447 | $39,333 | $108,041 | $68,708 |

### Review Scores by Department

| Department | Mean Review | Median Review | Reviews Available | Missing Reviews |
|-----------|------------|---------------|-------------------|-----------------|
| Engineering | 3.62 | 4.0 | 22 / 28 | 6 |
| Operations | 3.60 | 3.6 | 21 / 29 | 8 |
| Sales | 3.56 | 3.5 | 21 / 29 | 8 |
| HR | 3.46 | 3.5 | 30 / 35 | 5 |
| Marketing | 3.30 | 3.1 | 22 / 29 | 7 |

---

## 4. Comment / Feedback Analysis

- **Employees who left comments**: 69 (46.0%)
- **Employees with no comment**: 81 (54.0%)

### Comment Theme Distribution

| Theme | Count | % of Comments | Sentiment |
|-------|-------|--------------|-----------|
| More PTO please | 27 | 39.1% | Negative / Request |
| Need better tools | 22 | 31.9% | Negative / Request |
| Great place to work | 20 | 29.0% | Positive |

> Of those who commented, **71.0%** expressed a concern or request, while **29.0%** were positive.

### Comments by Department

| Department | More PTO please | Need better tools | Great place to work | Total Comments |
|-----------|----------------|-------------------|--------------------|--------------:|
| Engineering | 5 | 4 | 6 | 15 |
| HR | 7 | 5 | 3 | 15 |
| Marketing | 4 | 6 | 2 | 12 |
| Operations | 4 | 4 | 7 | 15 |
| Sales | 7 | 3 | 2 | 12 |

---

## 5. Key Correlations and Patterns

### Satisfaction vs. Salary
- Correlation coefficient: **-0.0127**
- Interpretation: Essentially **no linear relationship** between satisfaction and salary.

### Satisfaction vs. Review Score
- Correlation coefficient: **-0.2018**
- Interpretation: **Weak negative** relationship.

### Satisfaction by Tenure Band

| Tenure Band | Mean Satisfaction | Median | Respondents |
|------------|------------------|--------|-------------|
| 0-5 yrs | 3.96 | 4.0 | 24 |
| 6-10 yrs | 3.05 | 3.0 | 21 |
| 11-15 yrs | 3.21 | 3.0 | 33 |
| 16-20 yrs | 2.92 | 3.0 | 24 |
| 21+ yrs | 2.91 | 3.0 | 22 |

---

## 6. Flight Risk: High Performers with Low Satisfaction

Employees with a review score >= 4.0 but satisfaction rating <= 2 represent a **retention risk** -- they are valued contributors who may be looking to leave.

**14 employees** identified:

| EmployeeID | Department | Review Score | Satisfaction | Salary | Tenure | Comment |
|------------|-----------|-------------|-------------|--------|--------|---------|
| EMP-004 | HR | 4.4 | 2 | $104,220 | 16 yrs | -- |
| EMP-027 | HR | 4.3 | 2 | $81,555 | 11 yrs | -- |
| EMP-041 | Sales | 4.5 | 2 | $47,709 | 5 yrs | -- |
| EMP-063 | Engineering | 4.9 | 1 | $60,400 | 13 yrs | Need better tools |
| EMP-065 | Operations | 4.1 | 2 | $77,834 | 24 yrs | -- |
| EMP-067 | Operations | 5.0 | 1 | $66,029 | 15 yrs | Great place to work |
| EMP-079 | Engineering | 4.4 | 2 | $76,482 | 5 yrs | -- |
| EMP-082 | HR | 4.2 | 1 | $66,252 | 8 yrs | More PTO please |
| EMP-085 | HR | 4.9 | 1 | $71,107 | 10 yrs | -- |
| EMP-101 | Sales | 4.8 | 1 | $97,907 | 8 yrs | -- |
| EMP-112 | Operations | 4.6 | 2 | $49,940 | 23 yrs | -- |
| EMP-114 | Operations | 4.3 | 2 | $69,878 | 22 yrs | Great place to work |
| EMP-125 | Marketing | 4.8 | 1 | $44,154 | 17 yrs | -- |
| EMP-128 | Sales | 4.6 | 1 | $93,696 | 9 yrs | -- |

> **ACTION NEEDED**: These employees are performing well but are unhappy. Consider targeted retention conversations.

---

## 7. Low Satisfaction Deep Dive (Rating = 1)

**20 employees** gave the lowest possible satisfaction rating:

| EmployeeID | Department | Tenure | Salary | Review Score | Comment |
|------------|-----------|--------|--------|-------------|---------|
| EMP-010 | HR | 14 yrs | $81,581 | Missing | -- |
| EMP-017 | Engineering | 11 yrs | $75,952 | 2.1 | Need better tools |
| EMP-021 | Sales | 9 yrs | $82,752 | Missing | -- |
| EMP-024 | Sales | 17 yrs | $79,434 | Missing | More PTO please |
| EMP-026 | Operations | 13 yrs | $88,886 | Missing | More PTO please |
| EMP-030 | Marketing | 20 yrs | $94,002 | Missing | -- |
| EMP-037 | Sales | 19 yrs | $46,104 | 3.6 | -- |
| EMP-040 | HR | 16 yrs | $50,258 | 3.6 | -- |
| EMP-063 | Engineering | 13 yrs | $60,400 | 4.9 | Need better tools |
| EMP-067 | Operations | 15 yrs | $66,029 | 5.0 | Great place to work |
| EMP-078 | Marketing | 9 yrs | $95,239 | 2.7 | More PTO please |
| EMP-082 | HR | 8 yrs | $66,252 | 4.2 | More PTO please |
| EMP-084 | HR | 13 yrs | $49,446 | 2.3 | -- |
| EMP-085 | HR | 10 yrs | $71,107 | 4.9 | -- |
| EMP-095 | Engineering | 23 yrs | $87,879 | Missing | -- |
| EMP-101 | Sales | 8 yrs | $97,907 | 4.8 | -- |
| EMP-124 | Engineering | 17 yrs | $40,057 | Missing | More PTO please |
| EMP-125 | Marketing | 17 yrs | $44,154 | 4.8 | -- |
| EMP-128 | Sales | 9 yrs | $93,696 | 4.6 | -- |
| EMP-138 | Operations | 9 yrs | $65,082 | Missing | -- |

**Distribution by department:**

- HR: 5 employees (16.7% of rated employees in dept)
- Sales: 5 employees (20.0% of rated employees in dept)
- Engineering: 4 employees (16.0% of rated employees in dept)
- Operations: 3 employees (12.5% of rated employees in dept)
- Marketing: 3 employees (13.0% of rated employees in dept)

---

## 8. Key Flags and Recommendations for Leadership

### Critical Flags

1. **Significant Data Gaps**: 23 employees (15.3%) have no satisfaction rating, and 34 (22.7%) are missing review scores. This undermines the reliability of department-level conclusions. Investigate whether these are non-responses, new hires, or system issues.

2. **33.1% Dissatisfaction Rate**: Nearly a third of respondents rated satisfaction at 1 or 2. This is a significant proportion and suggests systemic issues, not isolated cases.

3. **PTO Is the Top Concern**: "More PTO please" is the most frequent comment theme (27 mentions, 39.1% of all comments). Consider benchmarking your PTO policy against industry standards.

4. **Tooling Complaints**: 22 employees cited needing better tools. This may be impacting both satisfaction and productivity. An infrastructure/tooling audit may be warranted, especially in departments with the most complaints.

5. **Retention Risk -- 14 High Performers Are Dissatisfied**: These employees have strong review scores (>= 4.0) but low satisfaction (<= 2). Losing these employees would directly impact team performance. Immediate 1:1 conversations recommended.

6. **Salary Outliers Detected**: 4 employee(s) have salaries significantly outside the normal range. Review for data accuracy or equity concerns.

7. **Department Disparity**: Operations has the lowest mean satisfaction (3.08), while Sales has the highest (3.32). This 0.24-point gap deserves targeted investigation in the underperforming department.

### Recommendations

1. **Immediate**: Conduct stay interviews with the identified flight-risk employees (high performers with low satisfaction)
2. **Short-term**: Benchmark and review PTO policy against industry peers; this is the single most common employee concern
3. **Short-term**: Conduct a tooling/infrastructure needs assessment, especially in Engineering and Operations
4. **Medium-term**: Investigate and close the data gaps -- ensure 100% survey completion and review score coverage
5. **Medium-term**: Deep-dive into Operations department to understand drivers of low satisfaction
6. **Ongoing**: Establish regular pulse surveys to track satisfaction trends over time, rather than relying on point-in-time snapshots

---

## Appendix: Data Summary Statistics

### Numeric Columns

| Statistic | YearsAtCompany | SatisfactionRating | Salary | LastReviewScore |
|-----------|---------------|-------------------|--------|----------------|
| count | 150.00 | 127.00 | $150 | 116.00 |
| mean | 12.85 | 3.21 | $74,935 | 3.50 |
| std | 7.05 | 1.41 | $27,336 | 0.85 |
| min | 0.00 | 1.00 | $33,911 | 2.00 |
| 25% | 7.00 | 2.00 | $61,920 | 2.70 |
| 50% | 13.00 | 3.00 | $70,981 | 3.55 |
| 75% | 18.75 | 4.50 | $83,504 | 4.30 |
| max | 25.00 | 5.00 | $247,729 | 5.00 |

---

*Report generated from employee_survey.csv (150 records). Analysis performed with pandas.*