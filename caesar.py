def encrypt(s, shift):
    return "".join(_shift_char(ch, shift) for ch in s)


def decrypt(s, shift):
    return encrypt(s, -shift)


def _shift_char(ch, shift):
    if "a" <= ch <= "z":
        base = ord("a")
    elif "A" <= ch <= "Z":
        base = ord("A")
    else:
        return ch

    return chr((ord(ch) - base + shift) % 26 + base)
