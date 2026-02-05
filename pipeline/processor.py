import logging
import numpy as np

from models.document import Document
from ocr.manager import OCRManager
from pipeline.layout_stage import LayoutAnalysisStage
from parsing.table_parser import TableParser
from extraction.structured_extractor import StructuredExtractor
from validation.accounting_validator import AccountingValidator
from confidence.engine import ConfidenceEngine

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Full document processing pipeline.
    """

    def __init__(self, ocr_manager: OCRManager):
        self.ocr_manager = ocr_manager
        self.layout_stage = LayoutAnalysisStage()
        self.table_parser = TableParser()
        self.extractor = StructuredExtractor()
        self.validator = AccountingValidator()
        self.confidence_engine = ConfidenceEngine()

    def process(self, image: np.ndarray, document_id: str) -> Document:
        logger.info("Starting full document processing")

        document = Document(document_id=document_id)

        # OCR
        document.ocr_result = self.ocr_manager.run(image)
        document.raw_text = document.ocr_result.full_text
        document.bump_version("ocr_completed")

        # Layout
        self.layout_stage.run(document)

        # Table parsing
        document.table_items = self.table_parser.parse(
            document.layout_metadata
        )
        document.bump_version("table_parsed")

        # Extraction
        extracted = self.extractor.extract(document)
        document.validation_report = extracted
        document.bump_version("data_extracted")

        # Validation
        self.validator.validate(document)

        # Confidence
        self.confidence_engine.calculate(document)

        logger.info("Document processing completed")
        return document
