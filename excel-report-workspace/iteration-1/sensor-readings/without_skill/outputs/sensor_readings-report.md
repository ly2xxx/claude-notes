# Sensor Readings Report

**Source file:** `excel-report-workspace/test-data/sensor_readings.csv`
**Date generated:** 2026-02-25
**Analysis period:** 2025-06-15 (single day, hourly readings)

---

## 1. Dataset Overview

| Property | Value |
|---|---|
| Total readings | 50 |
| Sensors | 3 (S-01, S-02, S-03) |
| Time span | 2025-06-15T00:00:00 to 2025-06-15T23:00:00 |
| Sampling interval | Hourly |
| Missing values | None detected |
| Columns | Timestamp, SensorID, Temperature_C, Humidity_Pct, Pressure_hPa |

### Readings per Sensor

| Sensor | Reading Count |
|---|---|
| S-01 | 15 |
| S-02 | 18 |
| S-03 | 17 |

**Note:** The timestamps appear to span multiple "cycles" of the same day (hours 0-23 repeat), suggesting the data may represent multiple days or repeated measurement cycles all dated 2025-06-15. There are approximately two complete 24-hour cycles across the 50 readings.

---

## 2. Overall Summary Statistics

| Metric | Temperature (C) | Humidity (%) | Pressure (hPa) |
|---|---|---|---|
| **Min** | 16.8 | 36.6 | 1000.0 |
| **Max** | 27.3 | 80.6 | 1021.8 |
| **Mean** | 21.3 | 55.0 | 1012.0 |
| **Range** | 10.5 | 44.0 | 21.8 |

### Key Takeaways

- **Temperature** ranged from 16.8 C to 27.3 C with a mean of 21.3 C, indicating mild conditions throughout the measurement period.
- **Humidity** showed the widest relative variability, spanning from 36.6% to 80.6%, a 44-percentage-point range. The mean of 55.0% suggests moderate humidity overall.
- **Pressure** stayed within a relatively narrow band (1000.0 to 1021.8 hPa), centered around 1012.0 hPa, which is close to standard atmospheric pressure (1013.25 hPa).

---

## 3. Per-Sensor Analysis

### 3.1 Sensor S-01 (15 readings)

| Metric | Temperature (C) | Humidity (%) | Pressure (hPa) |
|---|---|---|---|
| Min | 17.6 | 43.0 | 1008.8 |
| Max | 24.9 | 70.1 | 1018.0 |
| Mean | 20.7 | 55.8 | 1013.6 |

- S-01 recorded the **narrowest temperature range** (17.6-24.9 C, span of 7.3 C).
- Humidity was moderately variable (43.0-70.1%).
- Pressure was the most stable among all sensors, with the highest mean (1013.6 hPa).

### 3.2 Sensor S-02 (18 readings)

| Metric | Temperature (C) | Humidity (%) | Pressure (hPa) |
|---|---|---|---|
| Min | 18.1 | 36.6 | 1000.0 |
| Max | 27.3 | 70.8 | 1021.8 |
| Mean | 21.7 | 54.3 | 1011.3 |

- S-02 recorded the **highest temperature** in the dataset (27.3 C) and the **widest temperature range** (9.2 C).
- This sensor also captured the **lowest humidity** (36.6%) and the **lowest pressure** (1000.0 hPa).
- S-02 exhibited the most extreme pressure values in both directions, suggesting it may be located in a more variable microenvironment or have wider calibration tolerances.

### 3.3 Sensor S-03 (17 readings)

| Metric | Temperature (C) | Humidity (%) | Pressure (hPa) |
|---|---|---|---|
| Min | 16.8 | 38.8 | 1004.3 |
| Max | 25.4 | 80.6 | 1020.0 |
| Mean | 21.4 | 55.1 | 1011.5 |

- S-03 recorded the **lowest temperature** in the dataset (16.8 C) and the **highest humidity** (80.6%).
- The humidity spike to 80.6% at hour 07:00 is the single highest reading and stands out from the rest of the data.
- Mean pressure (1011.5 hPa) is slightly below the overall average.

---

## 4. Hourly Trends

The data contains readings across hours 0-23. Some hours have readings from multiple sensors, while others may have fewer. The following summarizes the average values per hour (across all sensors with data at that hour):

| Hour | Avg Temp (C) | Avg Humidity (%) | Avg Pressure (hPa) |
|---|---|---|---|
| 00 | 18.8 | 57.0 | 1014.2 |
| 01 | 19.2 | 46.3 | 1014.1 |
| 02 | 22.5 | 53.7 | 1018.4 |
| 03 | 22.4 | 55.5 | 1013.9 |
| 04 | 23.8 | 67.2 | 1005.6 |
| 05 | 19.7 | 43.0 | 1012.1 |
| 06 | 21.6 | 61.5 | 1014.9 |
| 07 | 21.2 | 66.7 | 1012.5 |
| 08 | 21.6 | 47.2 | 1011.6 |
| 09 | 22.5 | 55.6 | 1014.6 |
| 10 | 19.0 | 55.2 | 1008.5 |
| 11 | 19.6 | 55.2 | 1009.6 |
| 12 | 23.7 | 55.8 | 1014.0 |
| 13 | 21.2 | 48.0 | 1014.3 |
| 14 | 22.3 | 47.6 | 1010.9 |
| 15 | 21.3 | 56.7 | 1012.6 |
| 16 | 23.2 | 66.1 | 1013.7 |
| 17 | 21.5 | 57.4 | 1010.4 |
| 18 | 20.1 | 59.7 | 1010.8 |
| 19 | 20.6 | 54.7 | 1012.4 |
| 20 | 22.6 | 48.4 | 1015.6 |
| 21 | 22.9 | 47.0 | 1013.5 |
| 22 | 20.3 | 60.9 | 1005.0 |
| 23 | 23.8 | 57.9 | 1014.2 |

**Observations:**
- Temperature does not follow a strong diurnal pattern in this dataset, possibly because readings from different cycles/sensors overlap within the same hours.
- Humidity peaks around hours 04 and 07 (67.2% and 66.7% respectively).
- Pressure shows a dip around hours 10-11 and 22, with the lowest hourly average at hour 22 (1005.0 hPa).

---

## 5. Notable Observations and Potential Outliers

### Extreme Values

| Record | Sensor | Timestamp | Value |
|---|---|---|---|
| Highest temperature | S-02 | 2025-06-15T16:00:00 | 27.3 C |
| Lowest temperature | S-03 | 2025-06-15T05:00:00 | 16.8 C |
| Highest humidity | S-03 | 2025-06-15T07:00:00 | 80.6% |
| Lowest humidity | S-02 | 2025-06-15T14:00:00 | 36.6% |
| Highest pressure | S-02 | 2025-06-15T02:00:00 | 1021.8 hPa |
| Lowest pressure | S-02 | 2025-06-15T04:00:00 | 1000.0 hPa |

### Potential Outliers

- **Humidity 80.6% (S-03, hour 07):** This reading is notably higher than the dataset mean of 55.0% and significantly above the next-highest humidity reading (70.8%). It may warrant investigation -- possible condensation event or sensor anomaly.
- **Pressure 1000.0 hPa (S-02, hour 04):** This is the only pressure reading at exactly 1000.0 hPa and is 12 hPa below the dataset mean. This could indicate a localized low-pressure event or a sensor calibration issue. The round number (1000.0) also raises the possibility of a default/error value.
- **Temperature 27.3 C (S-02, hour 16):** While not extreme in absolute terms, this reading is 6.0 C above the mean and is the highest temperature recorded. S-02 also recorded the second-highest temperature (26.9 C), suggesting this sensor may be in a warmer location or have a slight high bias.

---

## 6. Data Quality Notes

1. **No missing values** were detected; all 50 rows contain complete data across all five columns.
2. **Timestamp anomaly:** All timestamps share the same date (2025-06-15), but there are more than 24 readings and hours repeat. This suggests the data may span multiple days with incorrect or simplified date encoding, or it represents multiple measurement cycles.
3. **Sensor distribution** is approximately even (15, 18, 17 readings), indicating balanced sampling across sensors.
4. **Value ranges** are all physically plausible for indoor or sheltered outdoor environmental monitoring.

---

## 7. Summary

This dataset contains 50 hourly environmental readings from three sensors (S-01, S-02, S-03) dated 2025-06-15. Conditions were mild overall, with temperatures averaging 21.3 C, humidity at 55.0%, and pressure near standard atmospheric at 1012.0 hPa. Sensor S-02 showed the widest variability across all three metrics, including the single lowest pressure reading (1000.0 hPa) which may deserve further investigation. Sensor S-03 captured the single highest humidity spike (80.6%) which stands out from the rest of the data. No missing data was detected, though the repeated timestamps within a single date suggest the dataset may represent multiple measurement cycles.
