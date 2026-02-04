# export/vat_breakdown.py

from collections import defaultdict


class VATBreakdownCalculator:

    @staticmethod
    def calculate(items):

        breakdown = defaultdict(lambda: {"net": 0.0, "vat": 0.0, "total": 0.0})

        for i in items:
            rate = i.vat_rate or 0.0

            breakdown[rate]["net"] += i.net_amount or 0.0
            breakdown[rate]["vat"] += i.vat_amount or 0.0
            breakdown[rate]["total"] += i.total_amount or 0.0

        return breakdown
