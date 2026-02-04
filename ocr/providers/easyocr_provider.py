import easyocr
from typing import List
from .base_provider import BaseOCRProvider, OCRResult


class EasyOCRProvider(BaseOCRProvider):

    def __init__(self):
        # Latin languages
        self.reader_latin = easyocr.Reader(['en', 'ro'])

        # Cyrillic languages
        self.reader_cyrillic = easyocr.Reader(['ru', 'en'])

    async def extract_text(self, images: List):

        results_text = []
        results_conf = []

        for img in images:

            # ---------- Latin OCR ----------
            latin_results = self.reader_latin.readtext(img)

            # ---------- Cyrillic OCR ----------
            cyrillic_results = self.reader_cyrillic.readtext(img)

            # Combine results
            combined = latin_results + cyrillic_results

            if not combined:
                continue

            text = " ".join([r[1] for r in combined])
            conf = sum([r[2] for r in combined]) / len(combined)

            results_text.append(text)
            results_conf.append(conf)

        return OCRResult(
            "\n".join(results_text),
            sum(results_conf) / len(results_conf) if results_conf else 0
        )
