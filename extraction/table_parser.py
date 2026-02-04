# extraction/table_parser.py

import re
from typing import List, Dict, Optional
from .normalizers import Normalizers


class TableParser:
    """
    Heuristic parser:
    - Detect rows with quantity + unit price + totals-like values
    - Conservative: only create items when >= 2 monetary tokens found
    """

    ROW_SPLIT = re.compile(r"\n+")
    MONEY_RE = re.compile(r"(\d{1,3}([ \.,]\d{3})*[\.,]\d{2})")
    QTY_RE = re.compile(r"\b(\d+([.,]\d+)?)\b")

    @staticmethod
    def parse_items(text: str) -> List[Dict]:
        items: List[Dict] = []
        rows = TableParser.ROW_SPLIT.split(text)

        for row in rows:
            monies = [m[0] for m in TableParser.MONEY_RE.findall(row)]
            if len(monies) < 2:
                continue

            qty_match = TableParser.QTY_RE.search(row)
            qty = Normalizers.normalize_money(qty_match.group(1)) if qty_match else None

            # Heuristic assignment: last money -> total, prev -> unit or net
            total = Normalizers.normalize_money(monies[-1])
            unit_or_net = Normalizers.normalize_money(monies[-2])

            description = re.sub(TableParser.MONEY_RE, "", row).strip()

            items.append({
                "description": description or None,
                "unit": None,
                "quantity": qty,
                "unit_price": unit_or_net if qty else None,
                "net_amount": None if qty else unit_or_net,
                "vat_rate": None,
                "vat_amount": None,
                "total_amount": total
            })

        return items
