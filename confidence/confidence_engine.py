# confidence/confidence_engine.py

import logging

from models.confidence_models import ConfidenceMetrics, RiskAnalysis

from .field_confidence import FieldConfidenceCalculator
from .document_confidence import DocumentConfidenceCalculator
from .risk_detector import RiskDetector


logger = logging.getLogger(__name__)


class ConfidenceEngine:

    def evaluate(self, data, validation_results, ocr_confidence):

        # -------------------------
        # Field scoring
        # -------------------------
        field_scores = {

            "supplier_name":
                FieldConfidenceCalculator.score_presence(data.supplier.name),

            "total_amount":
                FieldConfidenceCalculator.score_presence(data.totals.total_amount),

            "vat_amount":
                FieldConfidenceCalculator.score_presence(data.totals.vat_amount),

            "document_date":
                FieldConfidenceCalculator.score_presence(data.metadata.document_date),

            "iban":
                FieldConfidenceCalculator.score_presence(data.supplier.iban),

            "items":
                FieldConfidenceCalculator.score_items(data.items)
        }

        # -------------------------
        # Document score
        # -------------------------
        doc_score = DocumentConfidenceCalculator.calculate(field_scores)

        # Blend OCR reliability
        overall = (doc_score * 0.7) + (ocr_confidence * 0.3)

        # -------------------------
        # Risk detection
        # -------------------------
        risks = RiskDetector.detect(data, validation_results)

        logger.info(f"Document confidence: {overall}")

        return (
            ConfidenceMetrics(
                overall=round(overall, 2),
                fields=field_scores
            ),
            RiskAnalysis(risks=risks)
        )
