# ocr/providers/tesseract_provider.py

import pytesseract
from typing import List
from PIL import Image
from .base_provider import BaseOCRProvider, OCRResult


class TesseractProvider(BaseOCRProvider):

    async def extract_text(self, images: List[Image.Image]) -> OCRResult:

        texts = []
        confidences = []

        for img in images:
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

            text = " ".join(data["text"])
            conf_values = [float(c) for c in data["conf"] if c != "-1"]

            avg_conf = sum(conf_values) / len(conf_values) if conf_values else 0

            texts.append(text)
            confidences.append(avg_conf)

        final_text = "\n".join(texts)
        final_conf = sum(confidences) / len(confidences) if confidences else 0

        return OCRResult(final_text, final_conf)
