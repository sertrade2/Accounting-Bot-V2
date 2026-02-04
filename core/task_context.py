# core/task_context.py

from dataclasses import dataclass
from typing import Optional, List
from PIL import Image

from models.document_models import StructuredAccountingData
from models.validation_models import ValidationResults
from models.confidence_models import ConfidenceMetrics, RiskAnalysis


@dataclass
class ProcessingContext:

    images: List[Image.Image]

    ocr_text: Optional[str] = None
    ocr_confidence: Optional[float] = None
    ocr_provider: Optional[str] = None

    classification: Optional[dict] = None

    structured_data: Optional[StructuredAccountingData] = None

    validation_results: Optional[ValidationResults] = None

    confidence_metrics: Optional[ConfidenceMetrics] = None
    risk_analysis: Optional[RiskAnalysis] = None

    export_files: Optional[dict] = None
