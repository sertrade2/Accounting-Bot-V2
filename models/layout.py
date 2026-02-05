from dataclasses import dataclass
from typing import List, Literal, Tuple

from models.ocr import OCRBox

BlockType = Literal["HEADER", "TABLE", "FOOTER"]


@dataclass
class LayoutBlock:
    block_type: BlockType
    boxes: List[OCRBox]


@dataclass
class TableStructure:
    rows: List[List[OCRBox]]
    columns: List[List[OCRBox]]


@dataclass
class LayoutMetadata:
    header: LayoutBlock
    table: LayoutBlock
    footer: LayoutBlock
    table_structure: TableStructure
