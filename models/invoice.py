from dataclasses import dataclass
from typing import Optional


@dataclass
class InvoiceItem:
    description: str
    quantity: Optional[float]
    unit: Optional[str]
    unit_price: Optional[float]
    line_total: Optional[float]
    confidence: float
