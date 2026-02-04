# confidence/risk_detector.py

class RiskDetector:

    @staticmethod
    def detect(data, validation_results):

        risks = []

        # Validation failures
        if validation_results.status == "needs_review":
            risks.append("Validation issues detected")

        # Missing supplier ID
        if not data.supplier.vat_code and not data.supplier.idno:
            risks.append("Supplier tax identification missing")

        # Suspicious VAT
        if data.totals.vat_amount and data.totals.net_amount:
            ratio = data.totals.vat_amount / data.totals.net_amount

            if ratio > 0.30:
                risks.append("Unusually high VAT ratio")

        # Currency inconsistency
        if data.metadata.currency is None:
            risks.append("Currency not detected")

        # Missing totals
        if data.totals.total_amount is None:
            risks.append("Total amount missing")

        return risks
