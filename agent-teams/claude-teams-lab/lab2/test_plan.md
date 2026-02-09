# Test Plan for refactored_code.py

## Scope

Test the refactored `compute()` entry point, individual operation functions (`compute_sum`, `compute_avg`, `compute_max`), the `_validate_numbers()` helper, the `Operation` enum, and backward compatibility with the legacy `process()` function.

## Test Categories and Cases

### 1. Normal Operations via `compute()`

| # | Test Case | Input | Operation | Expected |
|---|-----------|-------|-----------|----------|
| 1.1 | Sum of positive integers | `[1, 2, 3]` | `"sum"` | `6.0` |
| 1.2 | Sum of positive floats | `[1.5, 2.5, 3.0]` | `"sum"` | `7.0` |
| 1.3 | Avg of positive integers | `[2, 4, 6]` | `"avg"` | `4.0` |
| 1.4 | Avg of positive floats | `[1.0, 2.0, 3.0]` | `"avg"` | `2.0` |
| 1.5 | Max of positive integers | `[3, 1, 2]` | `"max"` | `3.0` |
| 1.6 | Max of positive floats | `[1.5, 3.5, 2.5]` | `"max"` | `3.5` |

### 2. Individual Functions Directly

| # | Test Case | Function | Input | Expected |
|---|-----------|----------|-------|----------|
| 2.1 | compute_sum normal | `compute_sum` | `[1, 2, 3]` | `6.0` |
| 2.2 | compute_sum empty | `compute_sum` | `[]` | `0.0` |
| 2.3 | compute_avg normal | `compute_avg` | `[2, 4, 6]` | `4.0` |
| 2.4 | compute_avg empty | `compute_avg` | `[]` | `ValueError` |
| 2.5 | compute_max normal | `compute_max` | `[3, 1, 2]` | `3.0` |
| 2.6 | compute_max empty | `compute_max` | `[]` | `ValueError` |

### 3. Edge Cases

| # | Test Case | Input | Operation | Expected |
|---|-----------|-------|-----------|----------|
| 3.1 | Empty list sum | `[]` | `"sum"` | `0.0` |
| 3.2 | Empty list avg | `[]` | `"avg"` | `ValueError` |
| 3.3 | Empty list max | `[]` | `"max"` | `ValueError` |
| 3.4 | Single element sum | `[42]` | `"sum"` | `42.0` |
| 3.5 | Single element avg | `[42]` | `"avg"` | `42.0` |
| 3.6 | Single element max | `[42]` | `"max"` | `42.0` |
| 3.7 | Negative numbers sum | `[-1, -2, -3]` | `"sum"` | `-6.0` |
| 3.8 | Negative numbers avg | `[-4, -2]` | `"avg"` | `-3.0` |
| 3.9 | Negative numbers max | `[-5, -1, -3]` | `"max"` | `-1.0` |
| 3.10 | Mixed int/float | `[1, 2.5, 3]` | `"sum"` | `6.5` |
| 3.11 | All zeros | `[0, 0, 0]` | `"sum"` | `0.0` |
| 3.12 | Very large numbers | `[1e18, 1e18]` | `"sum"` | `2e18` |
| 3.13 | Tuple input (not just list) | `(1, 2, 3)` | `"sum"` | `6.0` |

### 4. Operation String & Enum Handling

| # | Test Case | Operation Arg | Expected |
|---|-----------|---------------|----------|
| 4.1 | Uppercase string "SUM" | `"SUM"` | Works, same as `"sum"` |
| 4.2 | Mixed case "Avg" | `"Avg"` | Works, same as `"avg"` |
| 4.3 | All caps "MAX" | `"MAX"` | Works, same as `"max"` |
| 4.4 | Operation.SUM enum | `Operation.SUM` | Works |
| 4.5 | Operation.AVG enum | `Operation.AVG` | Works |
| 4.6 | Operation.MAX enum | `Operation.MAX` | Works |

### 5. Error Handling

| # | Test Case | Input | Operation | Expected Error |
|---|-----------|-------|-----------|----------------|
| 5.1 | None as numbers | `None` | `"sum"` | `TypeError` |
| 5.2 | Non-numeric element (string) | `[1, "a", 3]` | `"sum"` | `TypeError` |
| 5.3 | None element in list | `[1, None, 3]` | `"sum"` | `TypeError` |
| 5.4 | Bool in list | `[1, True, 3]` | `"sum"` | `TypeError` |
| 5.5 | Unknown operation | `[1, 2]` | `"median"` | `ValueError` |
| 5.6 | Empty string operation | `[1, 2]` | `""` | `ValueError` |

### 6. `_validate_numbers()` Helper

| # | Test Case | Input | Expected |
|---|-----------|-------|----------|
| 6.1 | Valid list returned as list | `[1, 2, 3]` | `[1, 2, 3]` |
| 6.2 | Valid tuple converted to list | `(1, 2)` | `[1, 2]` |
| 6.3 | Empty list is valid | `[]` | `[]` |
| 6.4 | Non-sequence (int) | `42` | `TypeError` |
| 6.5 | Bool element rejected | `[True]` | `TypeError` |

### 7. Backward Compatibility with Legacy `process()`

For each combination below, verify `compute(data, op)` returns the same numeric value as `process(data, op)`:

| # | Data | Operations |
|---|------|-----------|
| 7.1 | `[1, 2, 3]` | sum, avg, max |
| 7.2 | `[10, 20, 30, 40]` | sum, avg, max |
| 7.3 | `[-5, 0, 5]` | sum, avg, max |
| 7.4 | `[1.5, 2.5]` | sum, avg, max |
| 7.5 | `[42]` | sum, avg, max |

### 8. Return Type Verification

All `compute()` return values must be `float` type (not int), verifying consistent return type.

## Implementation Approach

- Framework: `pytest`
- Use `pytest.raises` for error cases
- Use `pytest.approx` for float comparison where needed
- Import both `legacy_code.process` and `refactored_code.compute` for backward compat tests
- Group tests into classes by category
- Output file: `test_refactored.py`

## Total: ~42 test cases across 8 categories
