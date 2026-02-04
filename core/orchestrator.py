# core/orchestrator.py

from pathlib import Path
from PIL import Image

from core.pipeline import AccountingPipeline
from core.task_context import ProcessingContext


class AccountingOrchestrator:

    def __init__(self, cloud_ocr=None, llm_callable=None):

        self.pipeline = AccountingPipeline(
            cloud_ocr=cloud_ocr,
            llm_callable=llm_callable
        )

    async def process_file(self, file_path: str):

        images = self._load_images(file_path)

        context = ProcessingContext(images=images)

        base = Path("exports") / Path(file_path).stem
        base.parent.mkdir(exist_ok=True)

        result = await self.pipeline.run(
            context,
            str(base)
        )

        return self._build_output(result)

    # -------------------------------------
    # FILE LOADING
    # -------------------------------------
    def _load_images(self, file_path):

        ext = Path(file_path).suffix.lower()

        if ext in [".jpg", ".jpeg", ".png"]:
            return [Image.open(file_path)]

        # PDF support can be added here later
        raise ValueError("Unsupported file type")

    # -------------------------------------
    # FINAL OUTPUT FORMAT
    # -------------------------------------
    def _build_output(self, context):

        return {
            "document_classification": context.classification,
            "structured_accounting_data":
                context.structured_data.model_dump(),
            "validation_results":
                context.validation_results.model_dump(),
            "confidence_metrics":
                context.confidence_metrics.model_dump(),
            "risk_analysis":
                context.risk_analysis.model_dump(),
            "export_files": context.export_files
        }
