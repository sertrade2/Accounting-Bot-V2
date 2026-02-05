import logging
from models.document import Document
from layout.analyzer import LayoutAnalyzer

logger = logging.getLogger(__name__)


class LayoutAnalysisStage:
    """
    Pipeline stage: OCRResult → LayoutMetadata
    """

    def __init__(self):
        self.analyzer = LayoutAnalyzer()

    def run(self, document: Document) -> Document:
        if not document.ocr_result:
            raise ValueError("OCR result missing")

        logger.info("Running layout analysis stage")

        document.layout_metadata = self.analyzer.analyze(
            document.ocr_result
        )

        document.bump_version("layout_analysis")

        return document
