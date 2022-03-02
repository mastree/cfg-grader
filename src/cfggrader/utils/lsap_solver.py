from munkres import Munkres


class Munkres:
    solver = Munkres()

    @classmethod
    def compute(cls, matrix: list[list]):
        starred_indices = Munkres.solver.compute(matrix)
        total_cost = 0
        for x in starred_indices:
            total_cost += matrix[x[0]][x[1]]

        return total_cost, starred_indices
