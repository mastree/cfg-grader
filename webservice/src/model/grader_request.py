from webservice.src.model.graph_view import GraphView


class GraderRequest:
    def __init__(self, solution, jury_solutions):
        self.solution: GraphView = GraphView(**solution)
        self.jury_solutions: list[GraphView] = []

        for jury_solution in jury_solutions:
            self.jury_solutions.append(GraphView(**jury_solution))
