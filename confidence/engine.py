import logging
from typing import Dict

from models.document import Document
from confidence.weights import CONFIDENCE_WEIGHTS

logger = logging.getLogger(__name__)


class ConfidenceEngine:
    """
    Computes explainable confidence score for a document.
    """

    def calculate(self, document: Document) -> Dict[str, float]:
        logger.info("Calculating confidence score")

        breakdown: Dict[str, float] = {}

        # OCR confidence
        if document.ocr_result:
            breakdown["ocr"] = document.ocr_result.mean_confidence
        else:
            breakdown["ocr"] = 0.0

        # Structure confidence
        breakdown["structure"] = (
            1.0 if document.table_items else 0.4
        )

        # Math confidence
        if document.validation_report:
            breakdown["math"] = (
                1.0 if document.validation_report.get("valid") else 0.5
            )
        else:
            breakdown["math"] = 0.0

        # Supplier confidence (stub, improved in Phase 8)
        breakdown["supplier"] = 0.7

        total = 0.0
        for key, weight in CONFIDENCE_WEIGHTS.items():
            total += breakdown.get(key, 0.0) * weight

        breakdown["total"] = round(total, 3)

        document.confidence_breakdown = breakdown
        document.bump_version("confidence_calculated")

        logger.info(
            "Confidence calculated | total=%.2f",
            breakdown["total"],
        )

        return breakdown
