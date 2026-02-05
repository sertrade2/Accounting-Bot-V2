from typing import List
from models.ocr import OCRBox


def cluster_by_y(
    boxes: List[OCRBox],
    tolerance: int = 10,
) -> List[List[OCRBox]]:
    """
    Group OCR boxes into rows based on Y proximity.
    """
    rows: List[List[OCRBox]] = []

    for box in sorted(boxes, key=lambda b: b.bbox[1]):
        placed = False
        y_center = (box.bbox[1] + box.bbox[3]) // 2

        for row in rows:
            ref = row[0]
            ref_center = (ref.bbox[1] + ref.bbox[3]) // 2

            if abs(ref_center - y_center) <= tolerance:
                row.append(box)
                placed = True
                break

        if not placed:
            rows.append([box])

    return rows


def cluster_by_x(
    boxes: List[OCRBox],
    tolerance: int = 15,
) -> List[List[OCRBox]]:
    """
    Group OCR boxes into columns based on X proximity.
    """
    columns: List[List[OCRBox]] = []

    for box in sorted(boxes, key=lambda b: b.bbox[0]):
        placed = False
        x_center = (box.bbox[0] + box.bbox[2]) // 2

        for col in columns:
            ref = col[0]
            ref_center = (ref.bbox[0] + ref.bbox[2]) // 2

            if abs(ref_center - x_center) <= tolerance:
                col.append(box)
                placed = True
                break

        if not placed:
            columns.append([box])

    return columns
