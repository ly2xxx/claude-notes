"""Generate synthetic test datasets for the excel-report skill."""
import csv
import random
import os

random.seed(42)

os.makedirs("excel-report-workspace/test-data", exist_ok=True)

# --- Dataset 1: E-commerce orders (clean, typical business data) ---
statuses = ["Shipped", "Delivered", "Processing", "Cancelled", "Returned"]
categories = ["Electronics", "Clothing", "Home & Garden", "Books", "Sports"]
regions = ["North", "South", "East", "West"]

with open("excel-report-workspace/test-data/ecommerce_orders.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["OrderID", "Date", "Customer", "Region", "Category", "Amount", "Quantity", "Status"])
    for i in range(1, 201):
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        amount = round(random.gauss(85, 40), 2)
        # inject a few outliers
        if i in (15, 88, 142):
            amount = round(random.uniform(900, 1500), 2)
        if amount < 5:
            amount = 5.00
        qty = random.randint(1, 8)
        status = random.choices(statuses, weights=[30, 40, 15, 10, 5])[0]
        region = random.choice(regions)
        cat = random.choice(categories)
        w.writerow([
            f"ORD-{i:04d}",
            f"2025-{month:02d}-{day:02d}",
            f"Customer_{random.randint(100,999)}",
            region,
            cat,
            amount,
            qty,
            status,
        ])

# --- Dataset 2: Employee survey with missing values and messy data ---
departments = ["Engineering", "Sales", "Marketing", "HR", "Operations"]
ratings = [1, 2, 3, 4, 5]

with open("excel-report-workspace/test-data/employee_survey.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["EmployeeID", "Department", "YearsAtCompany", "SatisfactionRating", "Salary", "LastReviewScore", "Comments"])
    for i in range(1, 151):
        dept = random.choice(departments)
        years = random.randint(0, 25)
        satisfaction = random.choice(ratings) if random.random() > 0.15 else ""  # 15% missing
        salary = round(random.gauss(72000, 18000), 0)
        if i in (33, 77):
            salary = round(random.uniform(180000, 250000), 0)  # outliers
        review = round(random.uniform(2.0, 5.0), 1) if random.random() > 0.25 else ""  # 25% missing
        comment = random.choice(["", "", "", "Great place to work", "Need better tools", "More PTO please", ""])
        w.writerow([f"EMP-{i:03d}", dept, years, satisfaction, salary, review, comment])

# --- Dataset 3: Small, simple dataset (sensor readings) ---
with open("excel-report-workspace/test-data/sensor_readings.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Timestamp", "SensorID", "Temperature_C", "Humidity_Pct", "Pressure_hPa"])
    for i in range(50):
        hour = i % 24
        temp = round(random.gauss(22, 3), 1)
        humidity = round(random.gauss(55, 10), 1)
        pressure = round(random.gauss(1013, 5), 1)
        sid = random.choice(["S-01", "S-02", "S-03"])
        w.writerow([f"2025-06-15T{hour:02d}:00:00", sid, temp, humidity, pressure])

print("Test data generated:")
for name in ["ecommerce_orders.csv", "employee_survey.csv", "sensor_readings.csv"]:
    path = f"excel-report-workspace/test-data/{name}"
    with open(path) as f:
        lines = f.readlines()
    print(f"  {name}: {len(lines)-1} rows")
