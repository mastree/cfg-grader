import time

from cfggrader.utils.lsap_solver import Munkres
from cfggrader.classes.graph import Graph
from cfggrader.classes.graph_component import *
from cfggrader.cost_function import *
from classes.constants import *


class EditPath:
    def __init__(self, cost_function: CostFunction, source: Graph = None, target: Graph = None):
        self.source = source
        self.target = target

        self.unused_nodes1: list[Node] = []
        self.unused_edges1: list[Edge] = []
        self.unused_nodes2: list[Node] = []
        self.unused_edges2: list[Edge] = []

        self.cost_function = cost_function

    def init_root(self, sort_source: bool):
        tmp_unused_nodes1 = []
        self.unused_nodes2.extend(self.target.nodes)
        self.unused_edges1.extend(self.source.edges)
        self.unused_edges2.extend(self.target.edges)

        if sort_source:
            tmp_unused_nodes1.extend(self.source.nodes)

            matrix = self.build_node_matrix(tmp_unused_nodes1, self.unused_nodes2)
            Constants.FIRST_UB, starred_indices = Munkres.compute(matrix)

            starred_indices.sort(key=lambda x: matrix[x[0]][x[1]])
            for x in starred_indices:
                if x[0] < len(self.source.nodes):
                    self.unused_nodes1.append(tmp_unused_nodes1[x[0]])

        else:
            self.unused_nodes1.extend(self.source.nodes)

    def build_node_matrix(self, nodes1: list[Node], nodes2: list[Node]):
        size1 = len(nodes1)
        size2 = len(nodes2)

        msize = size1 + size2
        matrix = [[0.0] * msize for i in range(msize)]

        for i in range(size1):
            u = nodes1[i]
            for j in range(size2):
                v = nodes2[j]
                costs = self.cost_function.get_node_cost(u, v)
                edge_matrix = self.build_edge_matrix(u, v)

                edge_costs, _ = Munkres.compute(edge_matrix)
                costs += edge_costs
                matrix[i][j] = costs

        for i in range(size1, msize):
            u = Constants.NODE_EPS
            edge1 = Constants.EDGE_EPS
            for j in range(size2):
                if i - size1 == j:
                    v = nodes2[j]
                    costs = self.cost_function.get_node_cost(u, v)

                    # TODO: can be improved
                    edges = v.get_edges()
                    for edge2 in edges:
                        costs += self.cost_function.get_edge_cost(
                            edge1,
                            edge2,
                            edge1.from_node,
                            edge2.from_node
                        )

                    matrix[i][j] = costs
                else:
                    matrix[i][j] = Constants.INF

        for i in range(size1):
            u = nodes1[i]
            edges = u.get_edges()
            for j in range(size2, msize):
                if j - size2 == i:
                    v = Constants.NODE_EPS
                    edge2 = Constants.EDGE_EPS
                    costs = self.cost_function.get_node_cost(u, v)

                    # TODO: can be improved
                    for edge1 in edges:
                        costs += self.cost_function.get_edge_cost(
                            edge1,
                            edge2,
                            edge1.from_node,
                            edge2.from_node
                        )

                    matrix[i][j] = costs
                else:
                    matrix[i][j] = Constants.INF

        for i in range(size1, msize):
            for j in range(size2, msize):
                matrix[i][j] = 0.0

        return matrix

    def build_edge_matrix(self, node1: Node, node2: Node):
        edges1 = node1.get_edges()
        edges2 = node2.get_edges()
        size1 = len(edges1)
        size2 = len(edges2)
        msize = size1 + size2

        edge_matrix = [[0.0] * msize for i in range(msize)]

        for i in range(size1):
            edge1 = edges1[i]
            for j in range(size2):
                edge2 = edges2[j]
                edge_matrix[i][j] = self.cost_function.get_edge_cost(
                    edge1,
                    edge2,
                    edge1.from_node,
                    edge2.from_node
                )

        for i in range(size1, msize):
            edge1 = Constants.EDGE_EPS
            for j in range(size2):
                if i - size1 == j:
                    edge2 = edges2[j]
                    edge_matrix[i][j] = self.cost_function.get_edge_cost(
                        edge1,
                        edge2,
                        edge1.from_node,
                        edge2.from_node
                    )
                else:
                    edge_matrix[i][j] = Constants.INF

        for i in range(size1):
            edge1 = edges1[i]
            for j in range(size2, msize):
                if j - size2 == i:
                    edge2 = Constants.EDGE_EPS
                    edge_matrix[i][j] = self.cost_function.get_edge_cost(
                        edge1,
                        edge2,
                        edge1.from_node,
                        edge2.from_node
                    )
                else:
                    edge_matrix[i][j] = Constants.INF

        for i in range(size1, msize):
            for j in range(size2, msize):
                edge_matrix[i][j] = 0.0

        return edge_matrix


class DFSGED:
    def __init__(self, source: Graph, target: Graph, cost_function: CostFunction):
        self.source = source
        self.target = target
        self.cost_function = cost_function
        self.init()

        # time limit in milliseconds
        self.time_limit = 500

    def set_time_limit(self, time_limit):
        self.time_limit = time_limit

    def init(self):
        snode_size = len(self.source.nodes)
        tnode_size = len(self.target.nodes)
        sedge_size = len(self.source.edges)
        tedge_size = len(self.target.edges)

        Constants.node_cost_matrix = [[0] * (snode_size + 2) for i in range(tnode_size + 2)]
        Constants.edge_cost_matrix = [[0] * (sedge_size + 2) for i in range(tedge_size + 2)]

        # precompute node cost matrix
        for i in range(snode_size + 2):
            snode: Node = Constants.NODE_EPS
            if i < snode_size:
                snode = self.source.nodes[i]
            for j in range(tnode_size + 2):
                tnode: Node = Constants.NODE_EPS
                if j < tnode_size:
                    tnode = self.target.nodes[j]

                Constants.node_cost_matrix = self.cost_function.get_node_cost(snode, tnode)

        # precompute edge cost matrix
        for i in range(sedge_size + 2):
            sedge: Edge = Constants.EDGE_EPS
            if i < sedge_size:
                sedge = self.source.edges[i]
            for j in range(tedge_size + 2):
                tedge: Edge = Constants.EDGE_EPS
                if j < tedge_size:
                    tedge = self.target.edges[j]

                Constants.edge_cost_matrix = self.cost_function.get_edge_cost(
                    sedge,
                    tedge,
                    sedge.from_node,
                    tedge.from_node
                )

    def calculate_edit_distance(self):
        # start timer
        start_time = time.time_ns()

        # process
        snode_size = len(self.source.nodes)
        tnode_size = len(self.target.nodes)
        sedge_size = len(self.source.edges)
        tedge_size = len(self.target.edges)

        ub_cost = Constants.INF
        root = EditPath

        # end timer
        end_time = time.time_ns()
