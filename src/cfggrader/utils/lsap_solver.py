from munkres import Munkres
from cfggrader.classes.graph import Graph
from cfggrader.classes.graph_component import *


class Munkres:
    # Static Variables and Methods
    solver = Munkres()

    # Class Variables and methods
    def __init__(self, source: Graph = None, target: Graph = None):
        self.source = source
        self.target = target
        self.starred_indices: list = []

    def set_graphs(self, source: Graph, target: Graph):
        self.source = source
        self.target = target

    def set_source_graph(self, source: Graph):
        self.source = source

    def set_target_graph(self, target: Graph):
        self.target = target

    def compute(self, matrix: list[list]):
        self.starred_indices = self.solver.compute(matrix)
        total_cost = 0
        for x in self.starred_indices:
            total_cost += matrix[x[0]][x[1]]

        return total_cost

    def get_starred_indices(self):
        return self.starred_indices
