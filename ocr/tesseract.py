import pytesseract
import numpy as np
import logging

from models.ocr import OCRBox, OCRResult
from ocr.base import OCRProvider
from ocr.preprocessing import preprocess_image

logger = logging.getLogger(__name__)


class TesseractOCR(OCRProvider):
    name = "tesseract"

    def run(self, image: np.ndarray) -> OCRResult:
        logger.info("Running Tesseract OCR")

        processed = preprocess_image(image)

        data = pytesseract.image_to_data(
            processed,
            output_type=pytesseract.Output.DICT
        )

        boxes = []
        texts = []
        confidences = []

        for i in range(len(data["text"])):
            text = data["text"][i].strip()
            if not text:
                continue

            conf = float(data["conf"][i]) / 100.0
            x, y, w, h = (
                data["left"][i],
                data["top"][i],
                data["width"][i],
                data["height"][i],
            )

            boxes.append(
                OCRBox(
                    text=text,
                    confidence=conf,
                    bbox=(x, y, x + w, y + h),
                    line_id=data["line_num"][i],
                )
            )

            texts.append(text)
            confidences.append(conf)

        mean_conf = sum(confidences) / len(confidences) if confidences else 0.0

        result = OCRResult(
            full_text=" ".join(texts),
            boxes=boxes,
            mean_confidence=mean_conf,
            provider=self.name,
        )

        logger.info(
            "Tesseract OCR completed | confidence=%.2f",
            result.mean_confidence
        )

        return result
