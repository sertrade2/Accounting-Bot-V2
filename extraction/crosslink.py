# extraction/crosslink.py

from typing import List, Optional, Tuple


class CrossLinker:

    @staticmethod
    def sum_items_total(items: List[dict]) -> Optional[float]:
        vals = [i.get("total_amount") for i in items if isinstance(i.get("total_amount"), (int, float))]
        if not vals:
            return None
        return round(sum(vals), 2)

    @staticmethod
    def reconcile_totals(items: List[dict], totals: dict) -> dict:
        """
        If totals.total_amount missing but items sum exists → fill totals.total_amount.
        Never override existing totals unless None.
        """
        items_total = CrossLinker.sum_items_total(items)

        if totals.get("total_amount") is None and items_total is not None:
            totals["total_amount"] = items_total

        return totals
