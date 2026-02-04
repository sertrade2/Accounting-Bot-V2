# core/pipeline.py

import logging
from pathlib import Path

from core.task_context import ProcessingContext

from ocr.ocr_engine import MultiOCREngine
from classification.classifier import DocumentClassifier
from extraction.structured_extractor import StructuredAccountingExtractor
from memory.supplier_memory import SupplierMemoryEngine
from validation.accounting_validator import AccountingValidator
from confidence.confidence_engine import ConfidenceEngine
from export.export_orchestrator import ExportOrchestrator


logger = logging.getLogger(__name__)


class AccountingPipeline:

    def __init__(self, cloud_ocr=None, llm_callable=None):

        self.ocr = MultiOCREngine(cloud_ocr)
        self.classifier = DocumentClassifier()
        self.extractor = StructuredAccountingExtractor(llm_callable)
        self.memory = SupplierMemoryEngine()
        self.validator = AccountingValidator()
        self.confidence = ConfidenceEngine()
        self.exporter = ExportOrchestrator()

    # -----------------------------------------
    # MASTER PIPELINE
    # -----------------------------------------
    async def run(self, context: ProcessingContext, export_base_path: str):

        logger.info("Pipeline started")

        # -----------------------------------------
        # OCR
        # -----------------------------------------
        text, conf, provider = await self.ocr.process(context.images)

        context.ocr_text = text
        context.ocr_confidence = conf
        context.ocr_provider = provider

        # -----------------------------------------
        # Classification
        # -----------------------------------------
        classification = self.classifier.classify(text, conf)
        context.classification = classification

        # -----------------------------------------
        # Extraction
        # -----------------------------------------
        structured = await self.extractor.extract(
            text,
            classification.get("document_type")
        )

        # -----------------------------------------
        # Supplier Autofill
        # -----------------------------------------
        structured = self.memory.autofill(structured)

        context.structured_data = structured

        # -----------------------------------------
        # Validation
        # -----------------------------------------
        validation = self.validator.validate(structured)
        context.validation_results = validation

        # -----------------------------------------
        # Confidence + Risk
        # -----------------------------------------
        conf_metrics, risks = self.confidence.evaluate(
            structured,
            validation,
            conf
        )

        context.confidence_metrics = conf_metrics
        context.risk_analysis = risks

        # -----------------------------------------
        # Export
        # -----------------------------------------
        exports = self.exporter.export_all(
            structured,
            export_base_path
        )

        context.export_files = exports

        # -----------------------------------------
        # Memory Update
        # -----------------------------------------
        if validation.status == "ok":
            self.memory.update_memory(structured)

        logger.info("Pipeline completed")

        return context
