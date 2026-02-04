# validation/vat_validator.py

from decimal import Decimal
from typing import List, Tuple

from .rules_config import ALLOWED_VAT_RATES, DEFAULT_JURISDICTION, MONEY_TOLERANCE


class VATValidator:

    @staticmethod
    def validate_rates(items: List[dict], jurisdiction: str = DEFAULT_JURISDICTION) -> Tuple[list, list]:
        issues, warnings = [], []

        allowed = ALLOWED_VAT_RATES.get(jurisdiction, set())

        for idx, item in enumerate(items):
            rate = item.get("vat_rate")
            if rate is None:
                continue

            if float(rate) not in allowed:
                issues.append(f"Item {idx}: VAT rate {rate}% not allowed in {jurisdiction}.")

        return issues, warnings

    @staticmethod
    def validate_vat_math(items: List[dict]) -> Tuple[list, list]:
        issues, warnings = [], []

        for idx, i in enumerate(items):
            net = i.get("net_amount")
            rate = i.get("vat_rate")
            vat = i.get("vat_amount")

            if None in (net, rate, vat):
                continue

            expected = Decimal(str(net)) * (Decimal(str(rate)) / Decimal("100"))
            if abs(expected - Decimal(str(vat))) > Decimal(str(MONEY_TOLERANCE)):
                issues.append(f"Item {idx}: VAT amount incorrect.")

        return issues, warnings
