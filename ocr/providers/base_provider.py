# ocr/providers/base_provider.py

from abc import ABC, abstractmethod
from typing import List


class OCRResult:
    def __init__(self, text: str, confidence: float):
        self.text = text
        self.confidence = confidence


class BaseOCRProvider(ABC):

    @abstractmethod
    async def extract_text(self, images: List) -> OCRResult:
        pass
