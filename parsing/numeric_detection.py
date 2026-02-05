import re
from typing import Optional


NUMERIC_RE = re.compile(r"^-?\d+[.,]?\d*$")


def parse_number(text: str) -> Optional[float]:
    cleaned = text.replace(",", ".").strip()
    if NUMERIC_RE.match(cleaned):
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def is_numeric(text: str) -> bool:
    return parse_number(text) is not None
