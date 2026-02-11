# Code Review: main.py & Test Coverage

**Reviewer:** reviewer-main (Sonnet)
**Files reviewed:** `main.py`, `tests/` (absent)

---

## main.py

### Summary
Entry point that imports utilities and config, defines `process_data()` to calculate and format a total, and runs a demo with hardcoded data. Simple orchestration layer.

### What's Done Well
- Clean separation of concerns: config, utilities, and orchestration in separate modules
- Proper use of `if __name__ == "__main__":` guard
- Straightforward, readable flow

### Issues Found

#### Critical

*None*

#### Warning

1. **`tax_rate` from config is never applied**
   - `config.py` defines `tax_rate: 0.2` but `process_data` computes a raw sum with no tax calculation. This is either a missing feature or dead config.

   **Before:**
   ```python
   def process_data(items):
       total = calculate_total(items)
       return format_output(total, settings['currency'])
   ```

   **After (if tax should be applied):**
   ```python
   def process_data(items):
       subtotal = calculate_total(items)
       total = subtotal * (1 + settings['tax_rate'])
       return format_output(total, settings['currency'])
   ```

2. **No error handling** - If `settings` is missing the `'currency'` key, a `KeyError` is raised with no context. If `items` is not iterable, the error propagates from deep in `sum()`.

3. **Hardcoded demo data** - The `__main__` block uses `[100, 200, 300]` with no way to pass real data. For anything beyond a demo, this needs CLI args or file input.

#### Suggestion

1. **No type hints or docstring on `process_data`**:
   ```python
   def process_data(items: list[float]) -> str:
       """Calculate total of items and return formatted currency string."""
       total = calculate_total(items)
       return format_output(total, settings['currency'])
   ```

2. **Tight coupling to global `settings`** - `process_data` reads directly from the module-level `settings` dict. Passing config as a parameter would improve testability:
   ```python
   def process_data(items, currency=None):
       total = calculate_total(items)
       return format_output(total, currency or settings['currency'])
   ```

---

## Test Coverage: MISSING

**There is no `tests/` directory and no test files exist in this project.** This is a major gap.

### Recommended Test Structure

```
claude-teams-lab/
  tests/
    __init__.py
    test_utils.py
    test_main.py
    test_config.py
```

### Suggested Test Cases

#### test_utils.py
```python
import pytest
from utils import calculate_total, format_output


class TestCalculateTotal:
    def test_basic_sum(self):
        assert calculate_total([100, 200, 300]) == 600

    def test_empty_list(self):
        assert calculate_total([]) == 0

    def test_single_item(self):
        assert calculate_total([42]) == 42

    def test_negative_values(self):
        assert calculate_total([-10, 20, -5]) == 5

    def test_float_values(self):
        result = calculate_total([1.5, 2.5, 3.0])
        assert result == pytest.approx(7.0)

    def test_none_input(self):
        with pytest.raises(TypeError):
            calculate_total(None)

    def test_non_numeric_items(self):
        with pytest.raises(TypeError):
            calculate_total([1, "two", 3])


class TestFormatOutput:
    def test_basic_format(self):
        assert format_output(600) == "USD 600.00"

    def test_custom_currency(self):
        assert format_output(100, "EUR") == "EUR 100.00"

    def test_decimal_precision(self):
        assert format_output(99.999) == "USD 100.00"

    def test_zero(self):
        assert format_output(0) == "USD 0.00"

    def test_negative_value(self):
        assert format_output(-50) == "USD -50.00"

    def test_large_number(self):
        assert format_output(1000000) == "USD 1000000.00"
```

#### test_main.py
```python
from unittest.mock import patch
from main import process_data


class TestProcessData:
    def test_basic_processing(self):
        result = process_data([100, 200, 300])
        assert result == "USD 600.00"

    def test_empty_list(self):
        result = process_data([])
        assert result == "USD 0.00"

    @patch('main.settings', {'currency': 'EUR'})
    def test_respects_currency_config(self):
        result = process_data([50])
        assert result == "EUR 50.00"

    def test_float_items(self):
        result = process_data([10.5, 20.3])
        assert result == "USD 30.80"
```

#### test_config.py
```python
from config import settings


class TestConfig:
    def test_required_keys_exist(self):
        assert 'currency' in settings
        assert 'tax_rate' in settings
        assert 'debug' in settings

    def test_tax_rate_is_valid(self):
        assert 0 <= settings['tax_rate'] <= 1

    def test_currency_is_string(self):
        assert isinstance(settings['currency'], str)
        assert len(settings['currency']) == 3  # ISO 4217
```

### Coverage Priority
1. **High priority:** `calculate_total` and `format_output` — core logic
2. **Medium priority:** `process_data` — integration between modules
3. **Low priority:** Config validation — defensive but less critical
