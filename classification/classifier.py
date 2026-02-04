# classification/classifier.py

import logging
from collections import defaultdict

from .keyword_rules import DOCUMENT_KEYWORDS
from .structure_rules import StructureRules
from .language_detector import LanguageDetector
from .scoring import ClassificationScorer


logger = logging.getLogger(__name__)


class DocumentClassifier:

    def __init__(self):
        self.structure = StructureRules()

    def classify(self, ocr_text: str, ocr_confidence: float):

        scores = defaultdict(int)

        text_lower = ocr_text.lower()

        # --------------------------------
        # Keyword detection
        # --------------------------------
        for doc_type, keywords in DOCUMENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    scores[doc_type] += 3

        # --------------------------------
        # Structure detection
        # --------------------------------
        scores["invoice"] += self.structure.detect_invoice_patterns(ocr_text)
        scores["bank_statement"] += self.structure.detect_bank_patterns(ocr_text)

        # --------------------------------
        # Language signal
        # --------------------------------
        language = LanguageDetector.detect_language(ocr_text)

        if language in ["ro", "ru"]:
            scores["invoice"] += 1

        # --------------------------------
        # Determine best match
        # --------------------------------
        if not scores:
            return {
                "document_type": "unknown",
                "classification_confidence": 0
            }

        best_type = max(scores, key=scores.get)
        max_score = max(scores.values())

        confidence = ClassificationScorer.normalize(max_score, 10)
        confidence *= (ocr_confidence / 100)

        logger.info(
            f"Document classified as {best_type} "
            f"with confidence {confidence}"
        )

        return {
            "document_type": best_type,
            "classification_confidence": round(confidence, 2),
            "language": language
        }
