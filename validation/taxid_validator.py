# validation/taxid_validator.py

import re
from typing import Tuple

from .rules_config import TAX_ID_REGEX, DEFAULT_JURISDICTION


class TaxIDValidator:

    @staticmethod
    def _match(pattern_key: str, value: str) -> bool:
        pattern = TAX_ID_REGEX.get(pattern_key)
        return bool(pattern and re.match(pattern, value))

    @staticmethod
    def validate_party_ids(idno: str, vat_code: str, jurisdiction: str = DEFAULT_JURISDICTION) -> Tuple[list, list]:
        issues, warnings = [], []

        if jurisdiction == "MD":
            if idno and not TaxIDValidator._match("MD_IDNO", idno):
                issues.append("Supplier/Buyer IDNO format invalid for MD.")
            if vat_code and not TaxIDValidator._match("MD_VAT", vat_code):
                warnings.append("VAT code format unusual for MD.")

        if jurisdiction == "RO":
            if vat_code and not TaxIDValidator._match("RO_CUI", vat_code):
                issues.append("CUI format invalid for RO.")

        return issues, warnings
