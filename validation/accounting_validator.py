import logging
from typing import Dict, List

from models.document import Document
from models.invoice import InvoiceItem
from validation.rounding import approx_equal

logger = logging.getLogger(__name__)


class AccountingValidator:
    """
    ERP-grade accounting validation with explainable output.
    """

    def validate(self, document: Document) -> Dict[str, object]:
        logger.info("Running accounting validation")

        items = document.table_items or []
        report: Dict[str, object] = {
            "line_checks": [],
            "subtotal_check": None,
            "total_check": None,
            "valid": True,
        }

        # 1️⃣ Line-level validation
        for idx, item in enumerate(items, start=1):
            expected = None
            if item.quantity is not None and item.unit_price is not None:
                expected = round(item.quantity * item.unit_price, 2)

            ok = approx_equal(expected, item.line_total)

            report["line_checks"].append({
                "line": idx,
                "expected": expected,
                "actual": item.line_total,
                "valid": ok,
            })

            if not ok:
                report["valid"] = False

        # 2️⃣ Subtotal validation
        computed_subtotal = round(
            sum(i.line_total or 0.0 for i in items), 2
        )

        extracted_subtotal = document.validation_report.get("subtotal") \
            if document.validation_report else None

        if extracted_subtotal is not None:
            ok = approx_equal(computed_subtotal, extracted_subtotal)
            report["subtotal_check"] = {
                "computed": computed_subtotal,
                "extracted": extracted_subtotal,
                "valid": ok,
            }
            if not ok:
                report["valid"] = False

        document.validation_report = report
        document.bump_version("accounting_validated")

        logger.info(
            "Accounting validation completed | valid=%s",
            report["valid"],
        )

        return report
