# export/excel_exporter.py

import pandas as pd
from pathlib import Path

from models.document_models import StructuredAccountingData
from .vat_breakdown import VATBreakdownCalculator


class ExcelExporter:

    def export(self, data: StructuredAccountingData, output_path: str):

        path = Path(output_path)

        # -------------------------
        # SUMMARY SHEET
        # -------------------------
        summary = pd.DataFrame([{
            "Document Type": data.metadata.document_type,
            "Document Number": data.metadata.document_number,
            "Document Date": data.metadata.document_date,
            "Currency": data.metadata.currency,
            "Supplier": data.supplier.name,
            "Supplier VAT": data.supplier.vat_code,
            "Buyer": data.buyer.name,
            "Total Net": data.totals.net_amount,
            "Total VAT": data.totals.vat_amount,
            "Total Amount": data.totals.total_amount
        }])

        # -------------------------
        # LINE ITEMS SHEET
        # -------------------------
        items_df = pd.DataFrame([
            i.model_dump() for i in data.items
        ])

        # -------------------------
        # VAT BREAKDOWN
        # -------------------------
        vat_data = VATBreakdownCalculator.calculate(data.items)

        vat_df = pd.DataFrame([
            {
                "VAT Rate": k,
                "Net Amount": v["net"],
                "VAT Amount": v["vat"],
                "Total": v["total"]
            }
            for k, v in vat_data.items()
        ])

        # -------------------------
        # AUDIT SHEET
        # -------------------------
        audit_df = pd.DataFrame([{
            "Supplier IBAN": data.supplier.iban,
            "Supplier Address": data.supplier.address,
            "Buyer Address": data.buyer.address
        }])

        # -------------------------
        # WRITE FILE
        # -------------------------
        with pd.ExcelWriter(path, engine="openpyxl") as writer:

            summary.to_excel(writer, sheet_name="Summary", index=False)
            items_df.to_excel(writer, sheet_name="Items", index=False)
            vat_df.to_excel(writer, sheet_name="VAT Breakdown", index=False)
            audit_df.to_excel(writer, sheet_name="Audit", index=False)

        return str(path)
