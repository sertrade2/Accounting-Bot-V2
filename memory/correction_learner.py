# memory/correction_learner.py

class CorrectionLearner:

    @staticmethod
    def learn(existing_supplier: dict, corrected_supplier):

        corrections = existing_supplier.get("corrections", {})

        fields = ["name", "iban", "bank", "address", "vat_code"]

        for f in fields:
            new_val = getattr(corrected_supplier, f)

            if new_val:
                corrections[f] = new_val

        existing_supplier["corrections"] = corrections
        return existing_supplier
