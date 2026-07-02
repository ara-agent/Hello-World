"""Calculate common descriptive statistics."""

from collections import Counter
from math import sqrt
from collections.abc import Sequence
from typing import TypeVar


Number = int | float
ComparableNumber = TypeVar("ComparableNumber", int, float)


def mean(values: Sequence[Number]) -> float:
    """Return the arithmetic mean of values."""
    if not values:
        raise ValueError("mean requires at least one value")
    return sum(values) / len(values)


def median(values: Sequence[Number]) -> Number:
    """Return the median value."""
    if not values:
        raise ValueError("median requires at least one value")

    sorted_values = sorted(values)
    midpoint = len(sorted_values) // 2

    if len(sorted_values) % 2:
        return sorted_values[midpoint]

    return (sorted_values[midpoint - 1] + sorted_values[midpoint]) / 2


def mode(values: Sequence[ComparableNumber]) -> ComparableNumber:
    """Return the most common value, using the first-seen value to break ties."""
    if not values:
        raise ValueError("mode requires at least one value")

    counts = Counter(values)
    return counts.most_common(1)[0][0]


def stdev(values: Sequence[Number]) -> float:
    """Return the sample standard deviation of values."""
    if len(values) < 2:
        raise ValueError("stdev requires at least two values")

    average = mean(values)
    variance = sum((value - average) ** 2 for value in values) / (len(values) - 1)
    return sqrt(variance)
