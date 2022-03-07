from grader.src.cfggrader.classes.cost_function import CostFunction
from grader.src.cfggrader.classes.graph_component import *


class GeneralCostFunction(CostFunction):
    class Cost:
        EDGE_COST = 1
        NODE_COST = 1

    def __init__(self, use_node_relabel=True):
        super().__init__(use_node_relabel)

    def get_node_cost(self, a: Node, b: Node):
        if self.do_node_precompute:
            s_id = 0
            if a.is_not_eps():
                s_id = a.component_id
            t_id = 0
            if b.is_not_eps():
                t_id = b.component_id
            if self.node_precompute[s_id][t_id] < 0.0:
                self.node_precompute[s_id][t_id] = self._calculate_node_difference(a, b) * self.Cost.NODE_COST

            return self.node_precompute[s_id][t_id]

        return self._calculate_node_difference(a, b) * self.Cost.NODE_COST

    def get_edge_cost(self, a: Edge, b: Edge, a_node: Node, b_node: Node):
        # check if edge is epsilon
        if a.is_eps():
            if b.is_eps():
                return 0
            return self.Cost.EDGE_COST
        elif b.is_eps():
            return self.Cost.EDGE_COST

        # check if self loop
        if (a.from_node.get_id(), a.to_node.get_id()) == (a_node.get_id(), a_node.get_id()):
            if (b.from_node.get_id(), b.to_node.get_id()) == (b_node.get_id(), b_node.get_id()):
                return 0
            return 2 * self.Cost.EDGE_COST
        elif (b.from_node.get_id(), b.to_node.get_id()) == (b_node.get_id(), b_node.get_id()):
            return 2 * self.Cost.EDGE_COST

        # check if edge direction is the same
        if (a.from_node.get_id() == a_node.get_id()) == (b.from_node.get_id() == b_node.get_id()):
            return 0

        # edge deletion
        return 2 * self.Cost.EDGE_COST

    def get_edges_cost(self, a: list[Edge], b: list[Edge], a_node: Node, b_node: Node):
        if a_node.is_eps():
            if b_node.is_eps():
                return 0
            return self.Cost.EDGE_COST * len(b)
        elif b_node.is_eps():
            return self.Cost.EDGE_COST * len(a)

        type_count1 = self.count_each_edges_type(a, a_node)
        type_count2 = self.count_each_edges_type(b, b_node)
        remainder1 = 0
        remainder2 = 0
        for i in range(3):
            mn = min(type_count1[i], type_count2[i])
            type_count1[i] -= mn
            type_count2[i] -= mn
            remainder1 += type_count1[i]
            remainder2 += type_count2[i]

        return self.Cost.EDGE_COST * (remainder1 + remainder2)

    @classmethod
    def count_each_edges_type(cls, edges: list[Edge], node: Node):
        ret = [0, 0, 0]
        for edge in edges:
            t = edge.get_edge_type(node)
            ret[t] += 1
        return ret

    def _calculate_node_difference(self, a, b):
        if not self.use_node_relabel:
            return 0

        if a.is_eps():
            if b.is_eps():
                return 0
            return 1
        elif b.is_eps():
            return 1

        key = "label"
        n = len(a.info)
        m = len(b.info)
        max_dp = n + m

        dp = [[max_dp] * (m + 2) for i in range(n + 2)]  # dp[n + 2][m + 2]
        dpos_a = {}
        for i in range(n + 1):
            dp[i][0] = i

        for i in range(m + 1):
            dp[0][i] = i

        for i in range(1, n + 1):
            ca = a.info[i - 1][key]
            pos_b = 0
            for j in range(1, m + 1):
                cb = b.info[j - 1][key]
                pos_a = 0
                if cb in dpos_a:
                    pos_a = dpos_a[cb]

                diff = 1
                if ca == cb:
                    pos_b = j
                    diff = 0

                dp[i][j] = min(dp[i - 1][j] + 1,
                               dp[i][j - 1] + 1,
                               dp[i - 1][j - 1] + diff,
                               dp[pos_a - 1][pos_b - 1] + (i - pos_a - 1) + (j - pos_b - 1) + 1)

            dpos_a[ca] = i

        return dp[n][m] / max_dp
