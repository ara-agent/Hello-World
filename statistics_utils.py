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
