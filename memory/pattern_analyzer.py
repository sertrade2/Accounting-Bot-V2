# memory/pattern_analyzer.py

class PatternAnalyzer:

    @staticmethod
    def update_patterns(existing: dict, new_data):

        patterns = existing.get("patterns", {})

        # Currency pattern
        currency = new_data.metadata.currency
        if currency:
            patterns.setdefault("currencies", {})
            patterns["currencies"][currency] = patterns["currencies"].get(currency, 0) + 1

        # VAT pattern
        vat_rates = set(
            [i.vat_rate for i in new_data.items if i.vat_rate is not None]
        )

        if vat_rates:
            patterns.setdefault("vat_rates", {})
            for rate in vat_rates:
                patterns["vat_rates"][str(rate)] = patterns["vat_rates"].get(str(rate), 0) + 1

        existing["patterns"] = patterns
        return existing
