# classification/scoring.py

class ClassificationScorer:

    @staticmethod
    def normalize(score: float, max_score: float) -> float:
        if max_score == 0:
            return 0.0

        return round((score / max_score) * 100, 2)
