"""Detect normalized palindrome strings."""


def is_palindrome(s: str) -> bool:
    """Return True when s is a palindrome, ignoring case and punctuation."""
    cleaned = "".join(char.lower() for char in s if char.isalnum())
    return cleaned == cleaned[::-1]
