# classification/structure_rules.py

import re


class StructureRules:

    @staticmethod
    def detect_invoice_patterns(text: str) -> int:

        patterns = [
            r"VAT",
            r"TVA",
            r"TOTAL",
            r"SUBTOTAL",
            r"Unit price",
            r"Quantity"
        ]

        return sum(bool(re.search(p, text, re.IGNORECASE)) for p in patterns)


    @staticmethod
    def detect_bank_patterns(text: str) -> int:

        patterns = [
            r"IBAN",
            r"Account",
            r"Transaction",
            r"Balance"
        ]

        return sum(bool(re.search(p, text, re.IGNORECASE)) for p in patterns)
