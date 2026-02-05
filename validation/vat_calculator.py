from collections import defaultdict
from typing import Dict, List

from models.invoice import InvoiceItem


def calculate_vat_breakdown(
    items: List[InvoiceItem],
    vat_rates: Dict[str, float],
) -> Dict[float, float]:
    """
    Returns {vat_rate: vat_amount}
    """
    vat_totals = defaultdict(float)

    for item in items:
        if not item.line_total:
            continue

        rate = vat_rates.get(item.description, 0.0)
        vat_amount = item.line_total * rate / (100 + rate)
        vat_totals[rate] += round(vat_amount, 2)

    return dict(vat_totals)
