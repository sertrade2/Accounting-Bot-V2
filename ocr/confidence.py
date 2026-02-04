# ocr/confidence.py

class OCRConfidenceCalculator:

    @staticmethod
    def calculate(text_confidence: float, complexity: float) -> float:

        if complexity == 0:
            return text_confidence

        return round((text_confidence / complexity) * 100, 2)
