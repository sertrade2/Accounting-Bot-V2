# export/export_orchestrator.py

from models.document_models import StructuredAccountingData

from .excel_exporter import ExcelExporter
from .csv_exporter import CSVExporter
from .xml_exporter import XMLExporter


class ExportOrchestrator:

    def __init__(self):
        self.excel = ExcelExporter()
        self.csv = CSVExporter()
        self.xml = XMLExporter()

    def export_all(self, data: StructuredAccountingData, base_path: str):

        outputs = {}

        outputs["excel"] = self.excel.export(
            data,
            f"{base_path}.xlsx"
        )

        outputs["csv"] = self.csv.export(
            data,
            base_path + "_csv"
        )

        outputs["xml"] = self.xml.export(
            data,
            f"{base_path}.xml"
        )

        return outputs
