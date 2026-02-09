# Analysis of `legacy_code.py`

## Overview

The file contains a single function `process(data, type)` that performs one of three operations (sum, average, max) on a list of numbers based on a string flag. The function has significant issues across multiple categories.

---

## 1. Code Smells

### [Critical] Shadows built-in `type`
- **Line 1**: The parameter name `type` shadows Python's built-in `type()` function. This prevents use of `type()` within the function scope and is a well-known anti-pattern.
- **Recommendation**: Rename to `operation`, `mode`, or `strategy`.

### [Critical] Duplicated logic (DRY violation)
- **Lines 3-5 and 8-10**: The summation loop (`r = 0; for i in data: r = r + i`) is duplicated verbatim in both the `'sum'` and `'avg'` branches. This means any bug fix or change must be applied in two places.

### [Warning] Poor naming conventions
- `r` (lines 3, 8, 13) -- single-letter variable name; should be `result`, `total`, `current_max`, etc.
- `i` (lines 4, 9, 14) -- used as a value iterator, not an index. Convention is to use `i` for indices; a name like `value`, `item`, or `num` would be clearer.
- `process` -- extremely generic function name. Gives no indication of what it processes or how.
- `data` -- acceptable but could be more specific, e.g., `numbers` or `values`.

### [Warning] God function / monolithic design
- A single function handles three distinct operations via string-based dispatch. This violates the Single Responsibility Principle and makes the function harder to test, extend, and maintain.

### [Suggestion] Magic strings
- The operation types `'sum'`, `'avg'`, `'max'` are raw string literals with no validation. Typos like `'Sum'` or `'average'` silently return `None`. Consider using an `Enum` or constants.

---

## 2. Edge Cases and Bugs

### [Critical] ZeroDivisionError on empty list for `'avg'`
- **Line 11**: `return r / len(data)` -- if `data` is an empty list, `len(data)` is `0`, causing `ZeroDivisionError`. This is the most severe runtime bug.

### [Critical] IndexError on empty list for `'max'`
- **Line 13**: `r = data[0]` -- if `data` is an empty list, this raises `IndexError: list index out of range`.

### [Critical] TypeError on non-iterable input
- **Lines 4, 9, 14**: If `data` is `None`, an integer, or any non-iterable, the `for` loop raises `TypeError: 'NoneType' object is not iterable` (or similar). No input validation exists.

### [Warning] Silent failure on unknown operation
- **Lines 18-19**: Passing an unrecognized `type` string silently returns `None`. The caller has no way to distinguish between a legitimate `None` result and an invalid operation. This should raise a `ValueError`.

### [Warning] No handling of non-numeric elements
- If `data` contains strings, `None`, or mixed types, operations will raise `TypeError` at runtime with no helpful error message.

### [Suggestion] Empty list for `'sum'` returns 0
- **Line 3-6**: An empty list returns `0` for `'sum'`, which is mathematically correct but may be unexpected behavior depending on the domain. Worth documenting.

---

## 3. Design Problems

### [Critical] No separation of concerns
- Summation, averaging, and finding the maximum are three independent algorithms crammed into one function. Each should be its own function or handled via a strategy/dispatch pattern.

### [Warning] Not extensible
- Adding a new operation (e.g., `'min'`, `'median'`, `'std'`) requires modifying the function body and adding another `elif` branch. This violates the Open/Closed Principle. A dispatch dictionary or strategy pattern would allow extension without modification.

### [Warning] Reinvents built-in functionality
- Python provides `sum()`, `max()`, and `statistics.mean()` which are more efficient, better tested, and more readable. The manual loops are unnecessary.

### [Suggestion] No return type consistency
- The function returns `int | float | None` depending on the path. This makes it hard for callers to reason about the return type without careful inspection.

---

## 4. Best Practice Violations

### [Warning] No type hints
- **Line 1**: The function signature has no type annotations. Should be something like:
  ```
  def process(data: list[float], operation: str) -> float | None:
  ```

### [Warning] No docstring
- No documentation explaining what the function does, what parameters it expects, what it returns, or what exceptions it may raise.

### [Warning] No error handling
- Zero `try/except` blocks or input validation. Every failure mode produces an unhandled exception with no context.

### [Suggestion] No unit tests
- No corresponding test file exists. Given the multiple code paths, this function is at high risk of regressions.

### [Suggestion] Verbose loop patterns
- `r = 0; for i in data: r = r + i` could be `r = sum(data)`. The manual accumulation pattern is unnecessarily verbose.

---

## Summary Table

| # | Issue | Severity | Category | Line(s) |
|---|-------|----------|----------|---------|
| 1 | Shadows built-in `type` | Critical | Code Smell | 1 |
| 2 | Duplicated summation logic | Critical | Code Smell | 3-5, 8-10 |
| 3 | ZeroDivisionError on empty list (avg) | Critical | Bug | 11 |
| 4 | IndexError on empty list (max) | Critical | Bug | 13 |
| 5 | TypeError on None/non-iterable input | Critical | Bug | 4, 9, 14 |
| 6 | No separation of concerns | Critical | Design | 1-19 |
| 7 | Poor variable naming (`r`, `i`, `process`) | Warning | Code Smell | 1, 3, 4 |
| 8 | God function / monolithic design | Warning | Code Smell | 1-19 |
| 9 | Silent `None` on unknown operation | Warning | Bug | 18-19 |
| 10 | No handling of non-numeric elements | Warning | Bug | 4, 9, 14 |
| 11 | Not extensible (violates Open/Closed) | Warning | Design | 1-19 |
| 12 | Reinvents built-in functions | Warning | Design | 3-17 |
| 13 | No type hints | Warning | Best Practice | 1 |
| 14 | No docstring | Warning | Best Practice | 1 |
| 15 | No error handling | Warning | Best Practice | 1-19 |
| 16 | Magic strings for operation types | Suggestion | Code Smell | 2, 7, 12 |
| 17 | No unit tests | Suggestion | Best Practice | -- |
| 18 | Verbose loop patterns | Suggestion | Best Practice | 3-5, 8-10 |
| 19 | Inconsistent return type | Suggestion | Design | -- |

**Totals: 6 Critical, 9 Warning, 4 Suggestion**
