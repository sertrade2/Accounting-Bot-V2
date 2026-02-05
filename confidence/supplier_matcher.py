import logging
from typing import List, Optional

from rapidfuzz import fuzz

logger = logging.getLogger(__name__)


class SupplierMatcher:
    """
    Matches suppliers using fuzzy similarity.
    """

    def match(
        self,
        supplier: str,
        known_suppliers: List[str],
        threshold: int = 85,
    ) -> Optional[str]:
        best_score = 0
        best_match = None

        for known in known_suppliers:
            score = fuzz.token_sort_ratio(
                supplier.lower(), known.lower()
            )
            if score > best_score:
                best_score = score
                best_match = known

        if best_score >= threshold:
            logger.info(
                "Supplier matched | input=%s | match=%s | score=%d",
                supplier, best_match, best_score,
            )
            return best_match

        logger.info(
            "No supplier match | input=%s | best_score=%d",
            supplier, best_score,
        )
        return None
