import logging
import numpy as np
from typing import List

from ocr.base import OCRProvider
from models.ocr import OCRResult

logger = logging.getLogger(__name__)


class OCRManager:

    def __init__(
        self,
        providers: List[OCRProvider],
        confidence_threshold: float = 0.7,
        max_retries: int = 2,
    ):
        self.providers = providers
        self.confidence_threshold = confidence_threshold
        self.max_retries = max_retries

    def run(self, image: np.ndarray) -> OCRResult:
        last_result: OCRResult | None = None

        for provider in self.providers:
            for attempt in range(self.max_retries):
                try:
                    logger.info(
                        "OCR attempt | provider=%s | try=%d",
                        provider.name,
                        attempt + 1,
                    )

                    result = provider.run(image)
                    last_result = result

                    if result.is_confident(self.confidence_threshold):
                        logger.info(
                            "OCR accepted | provider=%s",
                            provider.name,
                        )
                        return result

                except Exception as e:
                    logger.exception(
                        "OCR failure | provider=%s | error=%s",
                        provider.name,
                        str(e),
                    )

        if last_result is None:
            raise RuntimeError("All OCR providers failed")

        logger.warning(
            "OCR fallback used | provider=%s | confidence=%.2f",
            last_result.provider,
            last_result.mean_confidence,
        )

        return last_result
