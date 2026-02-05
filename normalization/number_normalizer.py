from typing import Optional


def normalize_number(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None

    cleaned = (
        value.replace(" ", "")
        .replace(",", ".")
        .replace("O", "0")
        .replace("o", "0")
    )

    try:
        return float(cleaned)
    except ValueError:
        return None
