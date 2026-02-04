# models/confidence_models.py

from typing import Dict
from pydantic import BaseModel


class ConfidenceMetrics(BaseModel):
    overall: float
    fields: Dict[str, float]


class RiskAnalysis(BaseModel):
    risks: list[str]
