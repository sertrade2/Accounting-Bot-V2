# validation/accounting_validator.py

import logging
from typing import Tuple, List

from models.document_models import StructuredAccountingData
from models.validation_models import ValidationResults

from .math_validator import MathValidator
from .iban_validator import IBANValidator
from .vat_validator import VATValidator
from .taxid_validator import TaxIDValidator
from .rules_config import DEFAULT_JURISDICTION


logger = logging.getLogger(__name__)


class AccountingValidator:

    def __init__(self, jurisdiction: str = DEFAULT_JURISDICTION):
        self.jurisdiction = jurisdiction

    def validate(self, data: StructuredAccountingData) -> ValidationResults:
        issues: List[str] = []
        warnings: List[str] = []

        items = [i.model_dump() for i in data.items]
        totals = data.totals.model_dump()

        # -------------------------
        # Math validations
        # -------------------------
        i, w = MathValidator.validate_items_sum(items, totals)
        issues += i; warnings += w

        i, w = MathValidator.validate_net_vat_total(totals)
        issues += i; warnings += w

        # -------------------------
        # VAT validations
        # -------------------------
        i, w = VATValidator.validate_rates(items, self.jurisdiction)
        issues += i; warnings += w

        i, w = VATValidator.validate_vat_math(items)
        issues += i; warnings += w

        # -------------------------
        # IBAN validations
        # -------------------------
        for party_name, party in [("supplier", data.supplier), ("buyer", data.buyer)]:
            if party and party.iban:
                i, w = IBANValidator.validate(party.iban)
                issues += [f"{party_name}: {x}" for x in i]
                warnings += [f"{party_name}: {x}" for x in w]

        # -------------------------
        # Tax ID validations
        # -------------------------
        for party_name, party in [("supplier", data.supplier), ("buyer", data.buyer)]:
            if party:
                i, w = TaxIDValidator.validate_party_ids(
                    party.idno,
                    party.vat_code,
                    self.jurisdiction
                )
                issues += [f"{party_name}: {x}" for x in i]
                warnings += [f"{party_name}: {x}" for x in w]

        status = "ok" if not issues else "needs_review"

        logger.info(f"Validation completed. Status: {status}")

        return ValidationResults(
            status=status,
            issues=issues,
            warnings=warnings
        )
