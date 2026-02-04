# extraction/normalizers.py

import re
from datetime import datetime
from typing import Optional
from decimal import Decimal, InvalidOperation

from .schemas import ALLOWED_CURRENCIES


class Normalizers:

    @staticmethod
    def normalize_money(value: str) -> Optional[float]:
        """
        Accepts formats like:
        1 234,56 | 1,234.56 | 1234.56 | 1234,56
        """
        if not value:
            return None

        s = value.strip()
        # Remove spaces
        s = s.replace(" ", "")

        # Heuristic: if both , and . exist, assume last separator is decimal
        if "," in s and "." in s:
            if s.rfind(",") > s.rfind("."):
                s = s.replace(".", "").replace(",", ".")
            else:
                s = s.replace(",", "")
        else:
            # Only comma -> decimal comma
            if "," in s and "." not in s:
                s = s.replace(",", ".")
            # Only dot -> decimal dot (ok)

        try:
            return float(Decimal(s))
        except (InvalidOperation, ValueError):
            return None

    @staticmethod
    def normalize_date(value: str) -> Optional[str]:
        """
        Output strictly DD.MM.YYYY
        """
        if not value:
            return None

        candidates = [
            "%d.%m.%Y", "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%y", "%d/%m/%y"
        ]

        for fmt in candidates:
            try:
                d = datetime.strptime(value.strip(), fmt)
                return d.strftime("%d.%m.%Y")
            except ValueError:
                continue
        return None

    @staticmethod
    def normalize_currency(value: str) -> Optional[str]:
        if not value:
            return None
        v = value.strip().upper()
        return v if v in ALLOWED_CURRENCIES else None
