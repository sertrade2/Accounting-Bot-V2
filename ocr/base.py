from abc import ABC, abstractmethod
from typing import Any
import numpy as np

from models.ocr import OCRResult


class OCRProvider(ABC):

    name: str

    @abstractmethod
    def run(self, image: np.ndarray) -> OCRResult:
        """Run OCR and return structured OCRResult"""
        raise NotImplementedError
