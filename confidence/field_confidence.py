# confidence/field_confidence.py

class FieldConfidenceCalculator:

    @staticmethod
    def score_presence(value):
        return 100 if value else 0

    @staticmethod
    def score_items(items):
        if not items:
            return 0

        filled = 0
        total = len(items)

        for i in items:
            if i.total_amount:
                filled += 1

        return round((filled / total) * 100, 2)
