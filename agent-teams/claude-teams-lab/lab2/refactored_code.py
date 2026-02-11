"""Numeric operations on sequences of numbers.

Provides compute_sum, compute_avg, and compute_max as individual functions,
plus a unified compute() entry point with a dispatch-dict architecture
for easy extensibility.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from enum import Enum
from numbers import Number


class Operation(str, Enum):
    """Supported numeric operations."""

    SUM = "sum"
    AVG = "avg"
    MAX = "max"


def _validate_numbers(numbers: Sequence[float]) -> list[float]:
    """Validate and normalize the input sequence.

    Args:
        numbers: A sequence of numeric values.

    Returns:
        The input converted to a list of floats.

    Raises:
        TypeError: If numbers is not iterable or contains non-numeric values.
    """
    if not isinstance(numbers, (list, tuple, Sequence)):
        raise TypeError(
            f"numbers must be a sequence, got {type(numbers).__name__}"
        )
    for value in numbers:
        if not isinstance(value, Number) or isinstance(value, bool):
            raise TypeError(
                f"all elements must be numeric, got {type(value).__name__}: {value!r}"
            )
    return list(numbers)


def compute_sum(numbers: Sequence[float]) -> float:
    """Return the sum of numbers. Returns 0.0 for empty sequences."""
    return float(sum(numbers))


def compute_avg(numbers: Sequence[float]) -> float:
    """Return the arithmetic mean of numbers.

    Raises:
        ValueError: If the sequence is empty.
    """
    if len(numbers) == 0:
        raise ValueError("cannot compute avg of empty sequence")
    return float(sum(numbers) / len(numbers))


def compute_max(numbers: Sequence[float]) -> float:
    """Return the maximum value in the sequence.

    Raises:
        ValueError: If the sequence is empty.
    """
    if len(numbers) == 0:
        raise ValueError("cannot compute max of empty sequence")
    return float(max(numbers))


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
    validated = _validate_numbers(numbers)

    # Resolve string to Operation enum (case-insensitive)
    if isinstance(operation, str) and not isinstance(operation, Operation):
        try:
            operation = Operation(operation.lower())
        except ValueError:
            valid = ", ".join(op.value for op in Operation)
            raise ValueError(
                f"unknown operation {operation!r}, expected one of: {valid}"
            )

    func = OPERATIONS.get(operation)
    if func is None:
        valid = ", ".join(op.value for op in Operation)
        raise ValueError(
            f"unknown operation {operation!r}, expected one of: {valid}"
        )

    return func(validated)
