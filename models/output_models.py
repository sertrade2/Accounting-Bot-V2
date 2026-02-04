# models/output_models.py

from pydantic import BaseModel
from .document_models import StructuredAccountingData
from .validation_models import ValidationResults
from .confidence_models import ConfidenceMetrics, RiskAnalysis


class DocumentProcessingOutput(BaseModel):
    document_classification: dict
    structured_accounting_data: StructuredAccountingData
    validation_results: ValidationResults
    confidence_metrics: ConfidenceMetrics
    risk_analysis: RiskAnalysis
