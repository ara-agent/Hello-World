"""Run-length encoding helpers.

Escaping scheme:
    Each run is encoded as ``<count>:<hex-codepoint>;``. For example,
    ``"111aa"`` becomes ``"3:31;2:61;"``. Storing the character as a
    hexadecimal Unicode code point keeps digits and delimiter characters in
    the original string unambiguous.
"""


def encode(s):
    """Return a run-length encoded representation of ``s``."""
    if not s:
        return ""

    parts = []
    current = s[0]
    count = 1

    for char in s[1:]:
        if char == current:
            count += 1
        else:
            parts.append(f"{count}:{ord(current):x};")
            current = char
            count = 1

    parts.append(f"{count}:{ord(current):x};")
    return "".join(parts)


def decode(s):
    """Decode a string produced by :func:`encode`."""
    decoded = []
    i = 0

    while i < len(s):
        count_start = i
        while i < len(s) and s[i].isdigit():
            i += 1
        if count_start == i or i >= len(s) or s[i] != ":":
            raise ValueError("invalid RLE data")

        count = int(s[count_start:i])
        i += 1

        codepoint_start = i
        while i < len(s) and s[i] != ";":
            i += 1
        if codepoint_start == i or i >= len(s):
            raise ValueError("invalid RLE data")

        try:
            char = chr(int(s[codepoint_start:i], 16))
        except ValueError as exc:
            raise ValueError("invalid RLE data") from exc

        decoded.append(char * count)
        i += 1

    return "".join(decoded)
