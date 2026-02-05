from typing import Dict, List
from models.ocr import OCRBox
from parsing.numeric_detection import is_numeric


def infer_column_roles(
    columns: List[List[OCRBox]],
) -> Dict[int, str]:
    """
    Infer semantic role of each column by content pattern.
    """
    roles: Dict[int, str] = {}

    for idx, col in enumerate(columns):
        texts = [b.text for b in col]
        numeric_ratio = sum(is_numeric(t) for t in texts) / max(len(texts), 1)

        if numeric_ratio > 0.9:
            roles[idx] = "amount"
        elif numeric_ratio > 0.5:
            roles[idx] = "quantity"
        else:
            roles[idx] = "description"

    # Post-adjust: if multiple numeric columns, assign price/total
    numeric_cols = [i for i, r in roles.items() if r in ("amount", "quantity")]
    if len(numeric_cols) >= 2:
        roles[numeric_cols[-1]] = "line_total"
        roles[numeric_cols[-2]] = "unit_price"

    return roles
