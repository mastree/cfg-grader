from grader.src.cfggrader.classes.graph import Graph
from grader.src.cfggrader.classes.graph_component import *
import numpy as np


class CostFunction:
    def __init__(self, do_node_precompute: bool = False):
        self.do_node_precompute = do_node_precompute
        self.snode_size: int = None
        self.tnode_size: int = None
        self.node_precompute: list[list] = None

    def set_precompute(self, source: Graph, target: Graph):  # Graph component_id should be continuous from 0 to N - 1
        self.do_node_precompute = True

        self.snode_size = len(source.nodes)
        self.tnode_size = len(target.nodes)

        self.node_precompute = np.ndarray(shape=(self.snode_size + 1, self.tnode_size + 1), dtype=float)
        self.node_precompute.fill(-1.0)

    def get_node_cost(self, a: Node, b: Node):
        pass

    def get_edge_cost(self, a: Edge, b: Edge, a_node: Node, b_node: Node):
        pass

    def get_edges_cost(self, a: list[Edge], b: list[Edge], a_node: Node, b_node: Node):
        pass