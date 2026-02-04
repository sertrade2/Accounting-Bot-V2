# validation/math_validator.py

from typing import List, Tuple
from decimal import Decimal

from .rules_config import MONEY_TOLERANCE


class MathValidator:

    @staticmethod
    def _to_dec(v):
        return Decimal(str(v)) if v is not None else None

    @staticmethod
    def validate_items_sum(items: List[dict], totals: dict) -> Tuple[list, list]:
        issues, warnings = [], []

        items_total = sum(
            [MathValidator._to_dec(i.get("total_amount")) or Decimal("0")]
            for i in items
        )

        doc_total = MathValidator._to_dec(totals.get("total_amount"))

        if doc_total is None:
            warnings.append("Document total_amount is missing.")
            return issues, warnings

        if abs(items_total - doc_total) > Decimal(str(MONEY_TOLERANCE)):
            issues.append(
                f"Items total ({items_total}) does not match document total ({doc_total})."
            )

        return issues, warnings

    @staticmethod
    def validate_net_vat_total(totals: dict) -> Tuple[list, list]:
        issues, warnings = [], []

        net = MathValidator._to_dec(totals.get("net_amount"))
        vat = MathValidator._to_dec(totals.get("vat_amount"))
        total = MathValidator._to_dec(totals.get("total_amount"))

        if None in (net, vat, total):
            warnings.append("Net/VAT/Total incomplete for math validation.")
            return issues, warnings

        if abs((net + vat) - total) > Decimal(str(MONEY_TOLERANCE)):
            issues.append("Net + VAT does not equal Total.")

        return issues, warnings
