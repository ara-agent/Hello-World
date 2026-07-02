"""Utilities for checking anagrams."""


def are_anagrams(a, b):
    """Return True when a and b are anagrams, ignoring case and whitespace."""
    normalized_a = sorted("".join(str(a).lower().split()))
    normalized_b = sorted("".join(str(b).lower().split()))
    return normalized_a == normalized_b
