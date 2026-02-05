import logging
import re
from typing import Dict, Optional

from models.document import Document

logger = logging.getLogger(__name__)


class RuleBasedExtractor:
    """
    Fast deterministic extraction using known patterns.
    """

    VAT_RE = re.compile(r"VAT\s*(\d{1,2})\s*%", re.IGNORECASE)
    TOTAL_RE = re.compile(r"(total|итого)\s*[:\-]?\s*([\d.,]+)", re.IGNORECASE)

    def extract(self, document: Document) -> Dict[str, Optional[float]]:
        logger.info("Running rule-based extraction")

        text = document.raw_text or ""
        result: Dict[str, Optional[float]] = {}

        vat_match = self.VAT_RE.search(text)
        if vat_match:
            result["vat_rate"] = float(vat_match.group(1))

        total_match = self.TOTAL_RE.search(text)
        if total_match:
            result["total"] = self._parse_number(total_match.group(2))

        return result

    @staticmethod
    def _parse_number(value: str) -> Optional[float]:
        try:
            return float(value.replace(",", "."))
        except ValueError:
            return None
