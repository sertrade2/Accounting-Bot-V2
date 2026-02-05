import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class PatternLearner:
    """
    Learns correction patterns and reapplies them.
    """

    def __init__(self):
        self.patterns: Dict[str, str] = {}

    def learn(self, corrections: List[Dict[str, str]]) -> None:
        for c in corrections:
            key = f"{c['field']}::{c['original']}"
            self.patterns[key] = c["corrected"]

        logger.info(
            "Learned %d correction patterns",
            len(self.patterns),
        )

    def apply(self, field: str, value: str) -> str:
        key = f"{field}::{value}"
        return self.patterns.get(key, value)
