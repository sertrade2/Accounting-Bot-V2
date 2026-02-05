import logging
from typing import Dict

from models.document import Document

logger = logging.getLogger(__name__)


class LLMExtractor:
    """
    Fallback extraction using LLM when structure fails.
    """

    def extract(self, document: Document) -> Dict[str, float]:
        logger.warning("LLM fallback extraction triggered")

        # Placeholder hook — actual LLM call injected via provider
        raise RuntimeError(
            "LLM extraction not configured or disabled"
        )
