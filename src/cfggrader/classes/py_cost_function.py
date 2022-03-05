from cfggrader.classes.cost_function import CostFunction
from classes.constants import *


class Cost:
    EDGE_COST = 1
    NODE_COST = 1


class PyCostFunction(CostFunction):
    def get_node_cost(self, a: Node, b: Node):
        if self.do_node_precompute:
            s_id = self.snode_size
            if a.is_not_eps():
                s_id = a.component_id
            t_id = self.tnode_size
            if b.is_not_eps():
                t_id = b.component_id
            if self.node_precompute[s_id][t_id] < 0.0:
                self.node_precompute[s_id][t_id] = self.calculate_node_difference(a, b) * Cost.NODE_COST

            return self.node_precompute[s_id][t_id]

        return self.calculate_node_difference(a, b) * Cost.NODE_COST

    def get_edge_cost(self, a: Edge, b: Edge, a_node: Node, b_node: Node):
        # check if edge is epsilon
        if a.is_eps():
            if b.is_eps():
                return 0
            return Cost.EDGE_COST
        elif b.is_eps():
            return Cost.EDGE_COST

        # check if self loop
        if (a.from_node.get_id(), a.to_node.get_id()) == (a_node.get_id(), a_node.get_id()):
            if (b.from_node.get_id(), b.to_node.get_id()) == (b_node.get_id(), b_node.get_id()):
                return 0
            return 2 * Cost.EDGE_COST
        elif (b.from_node.get_id(), b.to_node.get_id()) == (b_node.get_id(), b_node.get_id()):
            return 2 * Cost.EDGE_COST

        # check if edge direction is the same
        if (a.from_node.get_id() == a_node.get_id()) == (b.from_node.get_id() == b_node.get_id()):
            return 0

        # edge deletion
        return 2 * Cost.EDGE_COST

    @classmethod
    def calculate_node_difference(cls, a, b):
        # TODO: change info key used
        # check if node is epsilon
        if a.is_eps():
            if b.is_eps():
                return 0
            return Cost.NODE_COST
        elif b.is_eps():
            return Cost.NODE_COST

        # check if node is the same (TODO: use edit distance for multipe line)
        # if a.info["rawLine"] == b.info["rawLine"]:
        #     return 0
        if len(a.info) == len(b.info):
            n = len(a.info)
            count = 0
            for i in range(n):
                if a.info[i]["rawLine"] != b.info[i]["rawLine"]:
                    count += 1
            return count / n

        return 1
