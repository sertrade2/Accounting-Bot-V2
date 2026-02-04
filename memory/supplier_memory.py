# memory/supplier_memory.py

import logging

from models.document_models import StructuredAccountingData
from .supplier_repository import SupplierRepository
from .supplier_matcher import SupplierMatcher
from .pattern_analyzer import PatternAnalyzer
from .correction_learner import CorrectionLearner


logger = logging.getLogger(__name__)


class SupplierMemoryEngine:

    def __init__(self):
        self.repo = SupplierRepository()

    # -------------------------------------
    # Autofill supplier data
    # -------------------------------------
    def autofill(self, data: StructuredAccountingData):

        supplier = data.supplier
        db = self.repo.get_all()

        key = SupplierMatcher.build_key(supplier)

        record = self.repo.get_supplier(key)

        # Fuzzy fallback
        if not record and supplier.name:
            fuzzy_key = SupplierMatcher.fuzzy_match(supplier.name, db)
            if fuzzy_key:
                record = db[fuzzy_key]

        if not record:
            return data

        corrections = record.get("corrections", {})

        for field, value in corrections.items():
            if getattr(supplier, field) is None:
                setattr(supplier, field, value)

        logger.info(f"Supplier autofill applied for {supplier.name}")
        return data

    # -------------------------------------
    # Save supplier after successful processing
    # -------------------------------------
    def update_memory(self, data: StructuredAccountingData):

        supplier = data.supplier
        key = SupplierMatcher.build_key(supplier)

        existing = self.repo.get_supplier(key) or {}

        # Save base info
        existing["name"] = supplier.name
        existing["idno"] = supplier.idno
        existing["vat_code"] = supplier.vat_code
        existing["iban"] = supplier.iban
        existing["bank"] = supplier.bank
        existing["address"] = supplier.address

        # Update patterns
        existing = PatternAnalyzer.update_patterns(existing, data)

        self.repo.save_supplier(key, existing)

        logger.info(f"Supplier memory updated: {supplier.name}")

    # -------------------------------------
    # Learn manual corrections
    # -------------------------------------
    def learn_corrections(self, original, corrected):

        key = SupplierMatcher.build_key(original)

        existing = self.repo.get_supplier(key) or {}

        existing = CorrectionLearner.learn(existing, corrected)

        self.repo.save_supplier(key, existing)

        logger.info(f"Corrections learned for supplier {corrected.name}")
