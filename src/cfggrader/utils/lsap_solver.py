from munkres import Munkres


class Munkres:
    # Static Variables and Methods
    solver = Munkres()

    # Class Variables and methods
    def __init__(self):
        self.starred_indices: list = []

    def compute(self, matrix: list[list]):
        self.starred_indices = self.solver.compute(matrix)
        total_cost = 0
        for x in self.starred_indices:
            total_cost += matrix[x[0]][x[1]]

        return total_cost

    def get_starred_indices(self):
        return self.starred_indices
