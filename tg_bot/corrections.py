import logging
from typing import Dict

from memory.correction_store import CorrectionStore
from memory.pattern_learner import PatternLearner

logger = logging.getLogger(__name__)

correction_store = CorrectionStore()
learner = PatternLearner()


def apply_correction(
    field: str,
    original: str,
    corrected: str,
    user_id: str,
) -> None:
    correction_store.save(
        field=field,
        original=original,
        corrected=corrected,
        user_id=user_id,
    )
    learner.learn(correction_store.all())
