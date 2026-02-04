# confidence/document_confidence.py

from .confidence_weights import FIELD_WEIGHTS


class DocumentConfidenceCalculator:

    @staticmethod
    def calculate(field_scores):

        total = 0

        for field, weight in FIELD_WEIGHTS.items():
            total += field_scores.get(field, 0) * weight

        return round(total, 2)
