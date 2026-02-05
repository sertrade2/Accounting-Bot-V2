import logging
from typing import Literal

from models.document import Document

logger = logging.getLogger(__name__)

DocumentType = Literal["invoice", "receipt", "unknown"]


class DocumentClassifier:
    """
    Classifies documents using layout + content signals.
    """

    def classify(self, document: Document) -> DocumentType:
        logger.info("Running document classification")

        # Layout signals
        has_table = bool(document.table_items)
        has_totals = (
            document.validation_report is not None
            and "total" in document.validation_report
        )

        if has_table and has_totals:
            return "invoice"

        if not has_table and document.raw_text:
            return "receipt"

        return "unknown"
