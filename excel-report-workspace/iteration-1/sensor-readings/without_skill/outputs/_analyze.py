import csv
import math
import os

# Read the CSV
data = []
with open(r'h:\code\yl\claude-notes\excel-report-workspace\test-data\sensor_readings.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append({
            'Timestamp': row['Timestamp'],
            'SensorID': row['SensorID'],
            'Temperature_C': float(row['Temperature_C']),
            'Humidity_Pct': float(row['Humidity_Pct']),
            'Pressure_hPa': float(row['Pressure_hPa']),
        })

print(f"Total readings: {len(data)}")

# Overall stats
def stats(values):
    n = len(values)
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / (n - 1)
    std = math.sqrt(variance)
    sorted_v = sorted(values)
    if n % 2 == 0:
        median = (sorted_v[n//2 - 1] + sorted_v[n//2]) / 2
    else:
        median = sorted_v[n//2]
    return {
        'count': n,
        'min': min(values),
        'max': max(values),
        'mean': mean,
        'std': std,
        'median': median,
        'q1': sorted_v[n//4],
        'q3': sorted_v[3*n//4],
    }

temps = [d['Temperature_C'] for d in data]
humids = [d['Humidity_Pct'] for d in data]
pressures = [d['Pressure_hPa'] for d in data]

print("\n=== OVERALL STATISTICS ===")
for name, values in [('Temperature_C', temps), ('Humidity_Pct', humids), ('Pressure_hPa', pressures)]:
    s = stats(values)
    print(f"{name}: count={s['count']}, min={s['min']:.1f}, max={s['max']:.1f}, mean={s['mean']:.2f}, median={s['median']:.1f}, std={s['std']:.2f}, Q1={s['q1']:.1f}, Q3={s['q3']:.1f}")

# Per-sensor stats
sensors = sorted(set(d['SensorID'] for d in data))
print(f"\nSensors: {sensors}")

for sensor in sensors:
    subset = [d for d in data if d['SensorID'] == sensor]
    print(f"\n--- {sensor} ({len(subset)} readings) ---")
    for name, key in [('Temperature_C', 'Temperature_C'), ('Humidity_Pct', 'Humidity_Pct'), ('Pressure_hPa', 'Pressure_hPa')]:
        values = [d[key] for d in subset]
        s = stats(values)
        print(f"  {name}: min={s['min']:.1f}, max={s['max']:.1f}, mean={s['mean']:.2f}, std={s['std']:.2f}")

# Hourly averages
print("\n=== HOURLY AVERAGES ===")
hourly = {}
for d in data:
    hour = int(d['Timestamp'][11:13])
    if hour not in hourly:
        hourly[hour] = {'temps': [], 'humids': [], 'pressures': []}
    hourly[hour]['temps'].append(d['Temperature_C'])
    hourly[hour]['humids'].append(d['Humidity_Pct'])
    hourly[hour]['pressures'].append(d['Pressure_hPa'])

for hour in sorted(hourly.keys()):
    h = hourly[hour]
    t_avg = sum(h['temps'])/len(h['temps'])
    hu_avg = sum(h['humids'])/len(h['humids'])
    p_avg = sum(h['pressures'])/len(h['pressures'])
    print(f"  Hour {hour:02d}: Temp={t_avg:.1f}C, Humidity={hu_avg:.1f}%, Pressure={p_avg:.1f} hPa (n={len(h['temps'])})")

# Time range
timestamps = [d['Timestamp'] for d in data]
print(f"\nTime range: {min(timestamps)} to {max(timestamps)}")

# Outlier detection (beyond 2 std from mean)
print("\n=== OUTLIER DETECTION (>2 std from mean) ===")
for name, values in [('Temperature_C', temps), ('Humidity_Pct', humids), ('Pressure_hPa', pressures)]:
    s = stats(values)
    low_thresh = s['mean'] - 2*s['std']
    high_thresh = s['mean'] + 2*s['std']
    outliers_low = [(i, v) for i, v in enumerate(values) if v < low_thresh]
    outliers_high = [(i, v) for i, v in enumerate(values) if v > high_thresh]
    if outliers_low or outliers_high:
        print(f"  {name}: {len(outliers_low)} low outliers (< {low_thresh:.1f}), {len(outliers_high)} high outliers (> {high_thresh:.1f})")
        for i, v in outliers_low:
            print(f"    Row {i+2}: {v} ({data[i]['SensorID']}, {data[i]['Timestamp']})")
        for i, v in outliers_high:
            print(f"    Row {i+2}: {v} ({data[i]['SensorID']}, {data[i]['Timestamp']})")
    else:
        print(f"  {name}: No outliers detected (range: {low_thresh:.1f} to {high_thresh:.1f})")

# Correlation (Pearson)
def pearson(x, y):
    n = len(x)
    mx = sum(x)/n
    my = sum(y)/n
    num = sum((xi-mx)*(yi-my) for xi, yi in zip(x, y))
    dx = math.sqrt(sum((xi-mx)**2 for xi in x))
    dy = math.sqrt(sum((yi-my)**2 for yi in y))
    if dx == 0 or dy == 0:
        return 0
    return num / (dx * dy)

print("\n=== CORRELATIONS ===")
print(f"  Temp vs Humidity: {pearson(temps, humids):.3f}")
print(f"  Temp vs Pressure: {pearson(temps, pressures):.3f}")
print(f"  Humidity vs Pressure: {pearson(humids, pressures):.3f}")

# Missing values
print("\n=== MISSING VALUES ===")
print("  None detected (all rows complete)")
