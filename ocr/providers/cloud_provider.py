# ocr/providers/cloud_provider.py

from .base_provider import BaseOCRProvider, OCRResult


class CloudOCRProvider(BaseOCRProvider):

    def __init__(self, provider_callable):
        self.provider_callable = provider_callable

    async def extract_text(self, images):

        text, confidence = await self.provider_callable(images)

        return OCRResult(text, confidence)
