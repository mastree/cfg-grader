class GraderResponse:
    def __init__(self, max_score: float, min_score: float, avg_score: float):
        self.max_score = max_score
        self.min_score = min_score
        self.avg_score = avg_score
