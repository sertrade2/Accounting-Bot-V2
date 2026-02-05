import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class CorrectionStore:
    """
    Stores user corrections with full audit trail.
    """

    def __init__(self):
        self._corrections: List[Dict[str, str]] = []

    def save(
        self,
        field: str,
        original: str,
        corrected: str,
        user_id: str,
    ) -> None:
        record = {
            "field": field,
            "original": original,
            "corrected": corrected,
            "user_id": user_id,
        }

        self._corrections.append(record)
        logger.info("Correction saved: %s", record)

    def all(self) -> List[Dict[str, str]]:
        return list(self._corrections)
