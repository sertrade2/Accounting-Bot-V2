from typing import Optional

UNIT_MAP = {
    "pcs": "шт",
    "pc": "шт",
    "шт.": "шт",
    "piece": "шт",
    "kg": "кг",
    "kgs": "кг",
    "кг.": "кг",
    "l": "л",
    "ltr": "л",
}


def normalize_unit(unit: Optional[str]) -> Optional[str]:
    if not unit:
        return None

    key = unit.strip().lower()
    return UNIT_MAP.get(key, unit)
