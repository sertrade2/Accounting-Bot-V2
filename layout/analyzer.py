import logging
from typing import List

from models.ocr import OCRBox, OCRResult
from models.layout import (
    LayoutBlock,
    LayoutMetadata,
    TableStructure,
)
from layout.clustering import cluster_by_x, cluster_by_y

logger = logging.getLogger(__name__)


class LayoutAnalyzer:
    """
    Detects HEADER / TABLE / FOOTER and reconstructs table layout.
    """

    def analyze(self, ocr: OCRResult) -> LayoutMetadata:
        logger.info("Starting layout analysis")

        boxes = ocr.boxes
        if not boxes:
            raise ValueError("No OCR boxes for layout analysis")

        # Step 1: cluster rows
        rows = cluster_by_y(boxes)

        # Step 2: identify table rows (largest dense block)
        table_rows = self._detect_table_rows(rows)

        table_boxes = [b for row in table_rows for b in row]
        header_boxes = [
            b for row in rows if row not in table_rows for b in row
            if row[0].bbox[1] < table_rows[0][0].bbox[1]
        ]
        footer_boxes = [
            b for row in rows if row not in table_rows for b in row
            if row[0].bbox[1] > table_rows[-1][0].bbox[1]
        ]

        # Step 3: detect columns inside table
        columns = cluster_by_x(table_boxes)

        layout = LayoutMetadata(
            header=LayoutBlock("HEADER", header_boxes),
            table=LayoutBlock("TABLE", table_boxes),
            footer=LayoutBlock("FOOTER", footer_boxes),
            table_structure=TableStructure(
                rows=table_rows,
                columns=columns,
            ),
        )

        logger.info(
            "Layout detected | header=%d | rows=%d | columns=%d | footer=%d",
            len(header_boxes),
            len(table_rows),
            len(columns),
            len(footer_boxes),
        )

        return layout

    def _detect_table_rows(
        self,
        rows: List[List[OCRBox]],
    ) -> List[List[OCRBox]]:
        """
        Heuristic: table = longest consecutive block of rows
        with similar column count.
        """
        best_block: List[List[OCRBox]] = []
        current_block: List[List[OCRBox]] = []

        prev_len = None

        for row in rows:
            length = len(row)

            if prev_len is None or abs(prev_len - length) <= 2:
                current_block.append(row)
            else:
                if len(current_block) > len(best_block):
                    best_block = current_block
                current_block = [row]

            prev_len = length

        if len(current_block) > len(best_block):
            best_block = current_block

        if not best_block:
            raise RuntimeError("Failed to detect table region")

        return best_block
