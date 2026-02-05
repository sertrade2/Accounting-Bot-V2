from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from models.ocr import OCRResult


@dataclass
class Document:
    document_id: str
    raw_text: str = ""

    # NEW (non-breaking)
    ocr_result: Optional[OCRResult] = None
    layout_metadata: Optional[Any] = None
    table_items: List[Any] = field(default_factory=list)
    validation_report: Optional[Dict[str, Any]] = None
    confidence_breakdown: Optional[Dict[str, float]] = None

    # Audit & versioning
    version: int = 1
    audit_log: List[Dict[str, Any]] = field(default_factory=list)

    def bump_version(self, reason: str) -> None:
        self.version += 1
        self.audit_log.append(
            {"version": self.version, "reason": reason}
        )
