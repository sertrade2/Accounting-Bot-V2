from typing import Optional

CURRENCY_MAP = {
    "rub": "RUB",
    "rur": "RUB",
    "₽": "RUB",
    "usd": "USD",
    "$": "USD",
    "eur": "EUR",
    "€": "EUR",
}


def normalize_currency(value: Optional[str]) -> Optional[str]:
    if not value:
        return None

    key = value.strip().lower()
    return CURRENCY_MAP.get(key, value.upper())
