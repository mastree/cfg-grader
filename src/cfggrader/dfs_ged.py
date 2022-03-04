import time

from cfggrader.classes.edit_path import EditPath
from cfggrader.classes.graph import Graph
from cfggrader.classes.cost_function import CostFunction
from classes.constants import Constants


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
