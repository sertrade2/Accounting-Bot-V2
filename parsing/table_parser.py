import logging
from typing import List

from models.layout import LayoutMetadata
from models.invoice import InvoiceItem
from models.ocr import OCRBox
from parsing.column_inference import infer_column_roles
from parsing.numeric_detection import parse_number

logger = logging.getLogger(__name__)


class TableParser:
    """
    Spatial table parser using bounding boxes and layout metadata.
    """

    def parse(self, layout: LayoutMetadata) -> List[InvoiceItem]:
        logger.info("Starting spatial table parsing")

        rows = layout.table_structure.rows
        columns = layout.table_structure.columns

        if not rows or not columns:
            logger.warning("No table structure detected")
            return []

        column_roles = infer_column_roles(columns)
        logger.debug("Inferred column roles: %s", column_roles)

        items: List[InvoiceItem] = []

        for row in rows:
            item = self._parse_row(row, column_roles)
            if item:
                items.append(item)

        logger.info("Parsed %d invoice items", len(items))
        return items

    def _parse_row(
        self,
        row: List[OCRBox],
        column_roles: dict[int, str],
    ) -> InvoiceItem | None:
        # Sort cells left → right
        cells = sorted(row, key=lambda b: b.bbox[0])

        data = {
            "description": [],
            "quantity": None,
            "unit": None,
            "unit_price": None,
            "line_total": None,
        }

        confidences = []

        for idx, cell in enumerate(cells):
            role = column_roles.get(idx, "description")
            text = cell.text
            confidences.append(cell.confidence)

            if role == "description":
                data["description"].append(text)

            elif role == "quantity":
                value = parse_number(text)
                if value is not None:
                    data["quantity"] = value

            elif role == "unit_price":
                value = parse_number(text)
                if value is not None:
                    data["unit_price"] = value

            elif role == "line_total":
                value = parse_number(text)
                if value is not None:
                    data["line_total"] = value

        description = " ".join(data["description"]).strip()
        if not description:
            return None

        confidence = sum(confidences) / len(confidences)

        return InvoiceItem(
            description=description,
            quantity=data["quantity"],
            unit=data["unit"],
            unit_price=data["unit_price"],
            line_total=data["line_total"],
            confidence=confidence,
        )
