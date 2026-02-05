import re
from typing import Optional


LEGAL_SUFFIXES = [
    r"\bllc\b",
    r"\bltd\b",
    r"\bgmbh\b",
    r"\bооо\b",
    r"\бао\b",
]


def normalize_supplier(name: Optional[str]) -> Optional[str]:
    if not name:
        return None

    result = name.lower()

    for suffix in LEGAL_SUFFIXES:
        result = re.sub(suffix, "", result, flags=re.IGNORECASE)

    result = re.sub(r"\s+", " ", result).strip()
    return result.title()
