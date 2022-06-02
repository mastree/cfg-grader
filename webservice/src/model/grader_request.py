from webservice.src.model.grading_method import GradingMethod
from webservice.src.model.graph_view import GraphView


class GraderRequest:
    def __init__(self, solution, references, timeLimit=5000, timeLimitPerUnit=3000, gradingMethod=GradingMethod.MAXIMUM.name, **kwargs):
        self.solution = GraphView(**solution)
        self.references: list[GraphView] = []
        self.time_limit = timeLimit
        self.time_limit_per_unit = max(self.time_limit // max(len(self.references), 1), timeLimitPerUnit)
        self.grading_method = GradingMethod[gradingMethod.upper()]

        for reference in references:
            self.references.append(GraphView(**reference))
