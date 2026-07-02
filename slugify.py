import re
import unicodedata


def slugify(s):
    normalized = unicodedata.normalize("NFKD", str(s))
    text = "".join(
        "-" if unicodedata.category(char)[0] in {"P", "Z"} else char
        for char in normalized
    )
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")
