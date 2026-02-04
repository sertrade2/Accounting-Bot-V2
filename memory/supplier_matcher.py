# memory/supplier_matcher.py

from rapidfuzz import fuzz


class SupplierMatcher:

    @staticmethod
    def build_key(supplier) -> str:
        if supplier.vat_code:
            return supplier.vat_code
        if supplier.idno:
            return supplier.idno
        if supplier.name:
            return supplier.name.lower()
        return "unknown"

    @staticmethod
    def fuzzy_match(name, db_suppliers):

        best_match = None
        best_score = 0

        for key, data in db_suppliers.items():
            score = fuzz.ratio(name.lower(), data.get("name", "").lower())

            if score > best_score and score > 85:
                best_match = key
                best_score = score

        return best_match
