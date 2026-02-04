# extraction/rule_extractors.py

import re
from typing import Dict, Optional, Tuple

from .normalizers import Normalizers


class RuleExtractors:

    MONEY_RE = re.compile(r"(\d{1,3}([ \.,]\d{3})*[\.,]\d{2})")
    DATE_RE = re.compile(r"(\d{2}[./-]\d{2}[./-]\d{2,4})")
    IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")
    VAT_RE = re.compile(r"\b(TVA|VAT)\b[:\s]*([\d]{1,2})\s?%?", re.IGNORECASE)
    DOC_NO_RE = re.compile(r"(No\.?|Nr\.?|№)\s*[:\-]?\s*([A-Z0-9\-\/]+)", re.IGNORECASE)
    CURRENCY_RE = re.compile(r"\b(MDL|EUR|USD|RON|RUB|UAH|GBP)\b", re.IGNORECASE)

    @staticmethod
    def extract_document_number(text: str) -> Optional[str]:
        m = RuleExtractors.DOC_NO_RE.search(text)
        return m.group(2) if m else None

    @staticmethod
    def extract_first_date(text: str) -> Optional[str]:
        m = RuleExtractors.DATE_RE.search(text)
        return Normalizers.normalize_date(m.group(1)) if m else None

    @staticmethod
    def extract_currency(text: str) -> Optional[str]:
        m = RuleExtractors.CURRENCY_RE.search(text)
        return Normalizers.normalize_currency(m.group(1)) if m else None

    @staticmethod
    def extract_totals(text: str) -> Dict[str, Optional[float]]:
        # Very common anchors; conservative to avoid hallucination
        anchors = {
            "net": r"(SUBTOTAL|NET|Fără TVA|Без НДС)[:\s]*" + RuleExtractors.MONEY_RE.pattern,
            "vat": r"(TVA|VAT)[:\s]*" + RuleExtractors.MONEY_RE.pattern,
            "total": r"(TOTAL|TOTAL DE PLATĂ|ИТОГО)[:\s]*" + RuleExtractors.MONEY_RE.pattern,
        }

        out = {"net_amount": None, "vat_amount": None, "total_amount": None}

        for k, pat in anchors.items():
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                money = m.group(2 if m.lastindex and m.lastindex >= 2 else 1)
                out_key = f"{k}_amount"
                out[out_key] = Normalizers.normalize_money(money)

        return out

    @staticmethod
    def extract_iban(text: str) -> Optional[str]:
        m = RuleExtractors.IBAN_RE.search(text)
        return m.group(0) if m else None
