import logging
from typing import Dict

from models.document import Document

logger = logging.getLogger(__name__)


class LayoutBasedExtractor:
    """
    Extracts totals, VAT, subtotal using layout signals.
    """

    def extract(self, document: Document) -> Dict[str, float]:
        logger.info("Running layout-based extraction")

        if not document.table_items:
            raise ValueError("No table items for layout extraction")

        subtotal = sum(
            item.line_total or 0.0 for item in document.table_items
        )

        return {
            "subtotal": round(subtotal, 2),
        }
