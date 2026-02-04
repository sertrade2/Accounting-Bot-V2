# ocr/ocr_engine.py

import logging
from typing import List
from PIL import Image

from .providers.tesseract_provider import TesseractProvider
from .providers.easyocr_provider import EasyOCRProvider
from .providers.cloud_provider import CloudOCRProvider
from .preprocess import ImagePreprocessor
from .confidence import OCRConfidenceCalculator


logger = logging.getLogger(__name__)


class MultiOCREngine:

    def __init__(self, cloud_callable=None):

        self.primary = TesseractProvider()
        self.secondary = EasyOCRProvider()
        self.cloud = CloudOCRProvider(cloud_callable) if cloud_callable else None

        self.conf_threshold = 70

    async def process(self, images: List[Image.Image]):

        # Preprocessing
        preprocessed = [
            ImagePreprocessor.preprocess(img)
            for img in images
        ]

        # PRIMARY
        result = await self.primary.extract_text(preprocessed)
        confidence = OCRConfidenceCalculator.calculate(result.confidence, 1.0)

        logger.info(f"Primary OCR confidence: {confidence}")

        if confidence >= self.conf_threshold:
            return result.text, confidence, "primary"

        # SECONDARY
        result = await self.secondary.extract_text(preprocessed)
        confidence = OCRConfidenceCalculator.calculate(result.confidence, 1.0)

        logger.warning(f"Secondary OCR used. Confidence: {confidence}")

        if confidence >= self.conf_threshold:
            return result.text, confidence, "secondary"

        # CLOUD FALLBACK
        if self.cloud:
            result = await self.cloud.extract_text(preprocessed)
            confidence = OCRConfidenceCalculator.calculate(result.confidence, 1.0)

            logger.error(f"Cloud OCR used. Confidence: {confidence}")

            return result.text, confidence, "cloud"

        return result.text, confidence, "low_confidence"
