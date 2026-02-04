# models/validation_models.py

from typing import List
from pydantic import BaseModel


class ValidationResults(BaseModel):
    status: str
    issues: List[str]
    warnings: List[str]
