# extraction/llm_extractor.py

import json
from typing import Optional, Dict, Any

from .schemas import LLM_SCHEMA_HINT


class LLMExtractor:
    """
    The llm_callable must:
      async def llm_callable(prompt: str) -> str  # returns JSON string
    """

    def __init__(self, llm_callable):
        self.llm_callable = llm_callable

    async def extract(self, ocr_text: str, doc_type: Optional[str]) -> Optional[Dict[str, Any]]:
        if not self.llm_callable:
            return None

        prompt = (
            "Extract accounting data strictly as JSON following this schema hint. "
            "If value not present in OCR text, return null. "
            "Never invent financial numbers. Dates must be DD.MM.YYYY. "
            f"Document type hint: {doc_type or 'unknown'}\n\n"
            f"Schema Hint:\n{json.dumps(LLM_SCHEMA_HINT, ensure_ascii=False)}\n\n"
            f"OCR TEXT:\n{ocr_text[:12000]}"  # truncate for safety
        )

        raw = await self.llm_callable(prompt)

        try:
            data = json.loads(raw)
            # Basic shape check
            if not isinstance(data, dict) or "metadata" not in data:
                return None
            return data
        except Exception:
            return None
