from cfggrader.classes.graph_component import *
from cfggrader.cost_function import CostFunction


class Constants:
    EDGE_COST = 1
    NODE_COST = 1

class PyCostFunction(CostFunction):
    def get_node_cost(self, a: Node, b: Node):
        return self.calculate_node_difference(a, b) * Constants.NODE_COST

    def get_edge_cost(self, a: Edge, b: Edge, a_node: Node, b_node: Node):
        if ((a.from_node == a_node) == (b.from_node == b_node)):
            return 0

        # edge deletion
        return 2 * Constants.EDGE_COST

    @classmethod
    def calculate_node_difference(cls, a, b):
        # TODO: change label
        if (a.info["rawLabel"] == b.info["rawLabel"]):
            return 0
        return 1
