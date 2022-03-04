from cfggrader.classes.graph import Graph
from cfggrader.classes.graph_component import *
from cfggrader.classes.cost_function import CostFunction
from cfggrader.utils.lsap_solver import Munkres
from classes.constants import Constants


class EditPath:
    @classmethod
    def create_path(cls, cost_function: CostFunction, source: Graph, target: Graph,
                    starred_indices: list):
        snode_len = len(source.nodes)
        sedge_len = len(source.edges)
        tnode_len = len(target.nodes)
        tedge_len = len(target.edges)

        edit_path = EditPath(cost_function, source, target)
        for x in starred_indices:
            snode = Constants.NODE_EPS
            if x[0] < snode_len:
                snode = source.nodes[x[0]]

            tnode = Constants.NODE_EPS
            if x[1] < tnode_len:
                tnode = target.nodes[x[1]]

            if snode.component_id is not None or tnode.component_id is not None:
                edit_path.add_distortion(snode, tnode)

        return edit_path

    @classmethod
    def create_root(cls, cost_function: CostFunction, source: Graph, target: Graph, sort_source: bool = True):
        edit_path = EditPath(cost_function, source, target)
        munkres = Munkres()

        # clear
        edit_path.unused_nodes1 = []
        tmp_unused_nodes1 = []

        if sort_source:
            tmp_unused_nodes1.extend(edit_path.source.nodes)

            matrix = edit_path.build_node_matrix(tmp_unused_nodes1, edit_path.unused_nodes2)
            total_cost = munkres.compute(matrix)
            starred_indices = munkres.get_starred_indices()

            starred_indices.sort(key=lambda x: matrix[x[0]][x[1]])
            for x in starred_indices:
                if x[0] < len(edit_path.source.nodes):
                    edit_path.unused_nodes1.append(tmp_unused_nodes1[x[0]])

        else:
            edit_path.unused_nodes1.extend(edit_path.source.nodes)

        return edit_path

    def __init__(self, cost_function: CostFunction, source: Graph = None, target: Graph = None):
        self.source = source
        self.target = target

        self.unused_nodes1: list[Node] = []
        self.unused_edges1: list[Edge] = []
        self.unused_nodes2: list[Node] = []
        self.unused_edges2: list[Edge] = []

        self.unused_edges1.extend(self.source.edges)
        self.unused_nodes2.extend(self.target.nodes)
        self.unused_edges1.extend(self.source.edges)
        self.unused_edges2.extend(self.target.edges)

        self.cost_function = cost_function

        self.total_cost = 0.0
        self.heuristic_cost = 0.0
        self.is_heuristic_computed = False

    def add_distortion(self, component1: GraphComponent, component2: GraphComponent):
        if isinstance(component1, Node):
            self.add_node_distortion(component1, component2)
        else:
            self.add_edge_distortion(component1, component2)

    def add_node_distortion(self, node1: Node, node2: Node):
        pass

    def add_edge_distortion(self, edge1: Edge, edge2: Edge):
        pass

    def build_node_matrix(self, nodes1: list[Node], nodes2: list[Node]):
        munkres = Munkres()

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

                edge_costs = munkres.compute(edge_matrix)
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
