# Refactoring Plan for `legacy_code.py`

## Before (Legacy)

A single monolithic `process(data, type)` function with 19 lines, string-based dispatch via if/elif, duplicated summation logic, no validation, no type hints, and 6 critical issues.

```python
def process(data, type):
    if type == 'sum':
        r = 0
        for i in data:
            r = r + i
        return r
    elif type == 'avg':
        ...
```

## After (Refactored)

A clean module with:
- An `Operation` enum for type-safe operation selection
- Individual operation functions for each computation
- A dispatch dictionary for extensibility (Open/Closed principle)
- A single public entry point `compute()` with full validation
- Proper type hints, docstrings, and error handling

## Proposed Module Structure

```
refactored_code.py
    - Operation (Enum): "sum", "avg", "max"
    - compute_sum(numbers) -> float
    - compute_avg(numbers) -> float
    - compute_max(numbers) -> float
    - OPERATIONS: dict[Operation, Callable]  (dispatch table)
    - compute(numbers, operation) -> float   (public entry point)
```

Single file, no over-engineering. No classes beyond the enum.

## Function Signatures

```python
from enum import Enum
from collections.abc import Sequence

class Operation(str, Enum):
    SUM = "sum"
    AVG = "avg"
    MAX = "max"

def compute_sum(numbers: Sequence[float]) -> float:
    """Return the sum of numbers. Returns 0.0 for empty sequences."""

def compute_avg(numbers: Sequence[float]) -> float:
    """Return the arithmetic mean. Raises ValueError if empty."""

def compute_max(numbers: Sequence[float]) -> float:
    """Return the maximum value. Raises ValueError if empty."""

OPERATIONS: dict[Operation, Callable[[Sequence[float]], float]] = {
    Operation.SUM: compute_sum,
    Operation.AVG: compute_avg,
    Operation.MAX: compute_max,
}

def compute(numbers: Sequence[float], operation: str | Operation) -> float:
    """Perform a numeric operation on a sequence of numbers.

    Args:
        numbers: A sequence of numeric values.
        operation: The operation to perform ("sum", "avg", or "max"),
                   either as a string or an Operation enum member.

    Returns:
        The computed result as a float.

    Raises:
        TypeError: If numbers is not iterable or contains non-numeric values.
        ValueError: If operation is unknown, or if the sequence is empty
                    for operations that require at least one element.
    """
```

## Edge Case Handling

| Edge Case | Legacy Behavior | Refactored Behavior |
|-----------|----------------|---------------------|
| `data=None` | TypeError (unhandled) | `TypeError("numbers must be a sequence, got NoneType")` |
| `data=[]` + avg | ZeroDivisionError | `ValueError("cannot compute avg of empty sequence")` |
| `data=[]` + max | IndexError | `ValueError("cannot compute max of empty sequence")` |
| `data=[]` + sum | Returns 0 | Returns `0.0` (documented) |
| Unknown operation | Silent `None` | `ValueError("unknown operation 'xyz', expected one of: sum, avg, max")` |
| Non-numeric elements | TypeError (unhandled) | `TypeError("all elements must be numeric")` |
| String operation "Sum" | Silent `None` | Case-insensitive: converts to lowercase before lookup |

## Design Decisions

1. **Dispatch dict over if/elif**: Adding a new operation (e.g., `min`) means adding one function and one dict entry -- no modification of existing logic.

2. **`str | Operation` for the operation param**: Accepts both raw strings (backward compatible) and enum members. Strings are converted to the enum internally.

3. **Use Python builtins**: `sum()` and `max()` instead of manual loops. `statistics.mean()` is avoided to keep dependencies minimal; simple `sum()/len()` is clear enough.

4. **Validate early**: Input validation happens in `compute()` so individual functions can trust their inputs. This avoids duplicating validation across every operation function.

5. **Always return float**: Consistent return type. `compute_sum([1, 2])` returns `3.0`, not `3`.

## What Gets Fixed

All 6 critical issues:
- [x] #1: `type` param renamed to `operation`
- [x] #2: Summation logic is not duplicated (uses `sum()`)
- [x] #3: ZeroDivisionError -> explicit ValueError
- [x] #4: IndexError -> explicit ValueError
- [x] #5: TypeError on None -> explicit TypeError with message
- [x] #6: Separated into individual functions + dispatch

All 9 warnings:
- [x] #7: Clear variable/function names
- [x] #8: No god function
- [x] #9: Unknown op raises ValueError
- [x] #10: Non-numeric elements caught in validation
- [x] #11: Extensible via dispatch dict
- [x] #12: Uses builtins
- [x] #13: Full type hints
- [x] #14: Docstrings on all functions
- [x] #15: Proper error handling with clear messages
