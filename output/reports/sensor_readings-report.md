# Data Report: sensor_readings.csv

## Executive Summary
This dataset contains 50 hourly sensor readings from three environmental sensors (S-01, S-02, S-03) recorded on June 15, 2025, capturing temperature, humidity, and barometric pressure. The data is fully complete with no missing values. The most notable finding is a single pressure outlier of 1000.0 hPa from sensor S-02, which falls below the expected range and may indicate a sensor malfunction or a genuine low-pressure weather event.

## Data Overview
| Property  | Value |
|-----------|-------|
| Rows      | 50    |
| Columns   | 5     |
| File type | CSV   |

### Column Descriptions
| Column | Detected Type | Non-Null Count | Description |
|--------|--------------|----------------|-------------|
| Timestamp | Datetime (string) | 50 | Hourly timestamps on 2025-06-15, ranging from 00:00 to 23:00. There are 24 unique hours, with multiple sensors reporting per hour. |
| SensorID | Categorical (string) | 50 | Identifier for the sensor device. Three unique values: S-01 (15 readings), S-02 (18 readings), S-03 (17 readings). |
| Temperature_C | Numeric (float64) | 50 | Temperature reading in degrees Celsius. |
| Humidity_Pct | Numeric (float64) | 50 | Relative humidity as a percentage. |
| Pressure_hPa | Numeric (float64) | 50 | Barometric pressure in hectopascals. |

### Numeric Column Statistics
| Statistic | Temperature_C | Humidity_Pct | Pressure_hPa |
|-----------|--------------|-------------|--------------|
| Min       | 16.80        | 36.60       | 1000.00      |
| Max       | 27.30        | 80.60       | 1021.80      |
| Mean      | 21.31        | 55.02       | 1012.44      |
| Median    | 20.60        | 56.40       | 1011.70      |
| Std Dev   | 2.66         | 10.16       | 4.39         |
| Q1 (25%)  | 19.10        | 46.78       | 1009.63      |
| Q3 (75%)  | 23.70        | 61.75       | 1015.20      |

### Categorical Column Summary
| Column | Unique Values | Top Values |
|--------|--------------|------------|
| SensorID | 3 | S-02 (18 readings, 36%), S-03 (17 readings, 34%), S-01 (15 readings, 30%) |

## Key Findings

### Notable Statistics
- **Temperature** ranges from 16.8 to 27.3 degrees C with a mean of 21.31 degrees C and moderate variability (std dev of 2.66). The distribution is roughly centered, with the median (20.60) close to the mean.
- **Humidity** varies widely from 36.6% to 80.6% with a mean of 55.02% and a standard deviation of 10.16, indicating substantial variation across readings.
- **Pressure** readings cluster tightly around 1012.44 hPa (std dev of 4.39), consistent with normal atmospheric pressure at sea level.

### Data Quality
- **No missing values** across any column -- the dataset is fully complete.
- **No duplicate rows** in the dataset.
- **Timestamp coverage**: All 24 hours of the day are represented, but readings are distributed unevenly across sensors (S-02 has 18 readings, S-01 has only 15).

### Outliers
- **Pressure_hPa**: One outlier detected at **1000.0 hPa** (from sensor S-02 at 04:00, second cycle). The IQR-based lower bound is 1001.26 hPa, making this reading statistically unusual. This is 12.44 hPa below the mean.
- **Temperature_C**: No outliers detected (all values within IQR bounds of 12.20 to 30.60).
- **Humidity_Pct**: No outliers detected (all values within IQR bounds of 24.31 to 84.21), although the maximum of 80.6% from sensor S-03 is notably high compared to most readings.

### Per-Sensor Patterns
- **S-01** (15 readings): Most stable sensor -- lowest temperature std dev (2.43) and lowest pressure std dev (2.65). Mean temperature of 20.73 degrees C.
- **S-02** (18 readings): Most readings and highest variability -- temperature ranges from 18.1 to 27.3 degrees C (std dev 3.10), and pressure has the highest std dev (5.39) including the 1000.0 hPa outlier. Mean temperature of 21.71 degrees C, the highest among all sensors.
- **S-03** (17 readings): Highest humidity variability (std dev 11.17) with the maximum humidity reading of 80.6%. Mean temperature of 21.39 degrees C.

## Recommendations
- **Investigate the 1000.0 hPa pressure outlier from S-02** -- verify whether this reflects a genuine atmospheric event or a sensor calibration issue. If S-02 consistently shows more pressure variability, it may need recalibration.
- **Balance sensor reading frequency** -- S-01 has 15 readings while S-02 has 18. If equal coverage is desired, check whether some S-01 readings were lost or if the sampling schedule is intentionally uneven.
- **Monitor S-03 humidity spikes** -- the 80.6% reading is not a statistical outlier but stands well above the typical range. If humidity accuracy is critical, consider cross-referencing S-03 humidity readings against a reference sensor.
- **Add date range coverage** -- all data is from a single day (June 15, 2025). For trend analysis, seasonal patterns, or anomaly detection, collecting data over a longer time window would be valuable.
- **Parse Timestamp as datetime** -- the Timestamp column is stored as a string. Converting it to a proper datetime type will enable time-series analysis, resampling, and temporal visualizations.
