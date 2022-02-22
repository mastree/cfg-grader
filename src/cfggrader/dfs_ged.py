from cfggrader.classes.graph import Graph
from cfggrader.classes.graph_component import *
from cfggrader.cost_function import *
from classes.constants import *


class DFSGED:
    def __init__(self, source: Graph, target: Graph, cost_function: CostFunction):
        self.source = source
        self.target = target
        self.cost_function = cost_function
        self.init()

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
            if (i < snode_size):
                snode = self.source.nodes[i]
            for j in range(tnode_size + 2):
                tnode: Node = Constants.NODE_EPS
                if (j < tnode_size):
                    tnode = self.target.nodes[j];

                Constants.node_cost_matrix = self.cost_function.get_node_cost(snode, tnode)

        # precompute edge cost matrix
        for i in range(sedge_size + 2):
            sedge: Edge = Constants.EDGE_EPS
            if (i < sedge_size):
                sedge = self.source.edges[i]
            for j in range(tedge_size + 2):
                tedge: Edge = Constants.EDGE_EPS
                if (j < tedge_size):
                    tedge = self.target.edges[j]

                Constants.edge_cost_matrix = self.cost_function.get_edge_cost(
                    sedge,
                    tedge,
                    sedge.from_node,
                    tedge.from_node)

    def calculate_edit_distance(self):
        pass
