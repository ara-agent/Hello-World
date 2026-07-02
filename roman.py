"""Roman numeral conversion utilities."""


def int_to_roman(n):
    """Convert an integer from 1 to 3999 into a Roman numeral."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("n must be an integer from 1 to 3999")
    if n < 1 or n > 3999:
        raise ValueError("n must be an integer from 1 to 3999")

    numerals = (
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    )

    result = []
    for value, numeral in numerals:
        count, n = divmod(n, value)
        result.append(numeral * count)
    return "".join(result)
