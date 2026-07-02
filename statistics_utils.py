from collections import Counter
from math import sqrt


def mean(values):
    if not values:
        raise ValueError("mean requires at least one value")
    return sum(values) / len(values)


def median(values):
    if not values:
        raise ValueError("median requires at least one value")

    sorted_values = sorted(values)
    midpoint = len(sorted_values) // 2

    if len(sorted_values) % 2:
        return sorted_values[midpoint]

    return (sorted_values[midpoint - 1] + sorted_values[midpoint]) / 2


def mode(values):
    if not values:
        raise ValueError("mode requires at least one value")

    counts = Counter(values)
    highest_count = max(counts.values())
    modes = [value for value, count in counts.items() if count == highest_count]
    return min(modes)


def stdev(values):
    if len(values) < 2:
        raise ValueError("stdev requires at least two values")

    average = mean(values)
    variance = sum((value - average) ** 2 for value in values) / (len(values) - 1)
    return sqrt(variance)
