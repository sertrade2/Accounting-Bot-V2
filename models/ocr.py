from dataclasses import dataclass
from typing import List, Tuple


BBox = Tuple[int, int, int, int]  # x1, y1, x2, y2


@dataclass(frozen=True)
class OCRBox:
    text: str
    confidence: float
    bbox: BBox
    line_id: int


@dataclass
class OCRResult:
    full_text: str
    boxes: List[OCRBox]
    mean_confidence: float
    provider: str

    def is_confident(self, threshold: float = 0.7) -> bool:
        return self.mean_confidence >= threshold
