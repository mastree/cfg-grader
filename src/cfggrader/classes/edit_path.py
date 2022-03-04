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

            if snode.is_not_eps() or tnode.is_not_eps():
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
            for i in range(len(matrix)):
                print(f'{i}: {matrix[i][i]}')
            total_cost = munkres.compute(matrix)
            print(total_cost)
            starred_indices = munkres.get_starred_indices()

            edit_path.first_ub = starred_indices

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

        # cost related
        self.cost_function = cost_function

        self.total_cost = 0.0
        self.heuristic_cost = 0.0
        self.is_heuristic_computed = False

        self.first_ub = []

        # distortion
        self.snode_distortion = {}
        self.sedge_distortion = {}
        self.tnode_distortion = {}
        self.tedge_distortion = {}

    def use_source_node(self, node: Node):
        self.unused_nodes1 = [x for x in self.unused_nodes1 if x.component_id != node.component_id]

    def use_target_node(self, node: Node):
        self.unused_nodes2 = [x for x in self.unused_nodes2 if x.component_id != node.component_id]

    def use_source_edge(self, edge: Edge):
        self.unused_edges1 = [x for x in self.unused_edges1 if x.component_id != edge.component_id]

    def use_target_edge(self, edge: Edge):
        self.unused_edges2 = [x for x in self.unused_edges2 if x.component_id != edge.component_id]

    def add_distortion(self, component1: GraphComponent, component2: GraphComponent):
        if isinstance(component1, Node):
            self.add_node_distortion(component1, component2)
        else:
            self.add_edge_distortion(component1, component2)

    def add_node_distortion(self, node1: Node, node2: Node):
        self.is_heuristic_computed = False

        self.total_cost += self.cost_function.get_node_cost(node1, node2)
        if node1.is_not_eps():
            self.snode_distortion[node1] = node2
            self.use_source_node(node1)
        if node2.is_not_eps():
            self.tnode_distortion[node2] = node1
            self.use_target_node(node2)

        if node1.is_eps() and node2.is_eps():
            return

        # handle edges
        # node deletion
        if node2.is_eps():
            for edge in node1.edges:
                onode1 = edge.get_other_end(node1)
                if onode1 in self.snode_distortion:
                    self.add_edge_distortion(edge, Constants.EDGE_EPS, node1, Constants.NODE_EPS)
            return

        # node insertion
        if node1.is_eps():
            for edge in node2.edges:
                onode2 = edge.get_other_end(node2)
                if onode2 in self.tnode_distortion:
                    self.add_edge_distortion(Constants.EDGE_EPS, edge, Constants.NODE_EPS, node2)
            return

        for edge1 in node1.edges:
            onode1 = edge1.get_other_end(node1)
            is_out_edge = edge1.from_node.component_id == node1.component_id
            if onode1 in self.snode_distortion:
                onode2 = self.snode_distortion[onode1]
                if onode2.is_eps():
                    self.add_edge_distortion(edge1, Constants.EDGE_EPS, node1, Constants.NODE_EPS)
                else:
                    edge2: Edge = None
                    if is_out_edge:
                        edge2 = node2.get_edge_to(onode2)
                    else:
                        edge2 = onode2.get_edge_to(node2)

                    if edge2 is None:
                        self.add_edge_distortion(edge1, Constants.EDGE_EPS, node1, Constants.NODE_EPS)
                    else:
                        self.add_edge_distortion(edge1, edge2, node1, node2)

        for edge2 in node2.edges:
            onode2 = edge2.get_other_end(node2)
            is_out_edge = edge2.from_node.component_id == node2.component_id
            if onode2 in self.tnode_distortion:
                onode1 = self.tnode_distortion[onode2]
                if onode1.is_not_eps():
                    edge1: Edge = None
                    if is_out_edge:
                        edge1 = node1.get_edge_to(onode1)
                    else:
                        edge1 = onode1.get_edge_to(node1)

                    if edge1 is None:
                        self.add_edge_distortion(Constants.EDGE_EPS, edge2, Constants.NODE_EPS, node2)

    def add_edge_distortion(self, edge1: Edge, edge2: Edge, node1: Node, node2: Node):
        self.is_heuristic_computed = False

        self.total_cost += self.cost_function.get_edge_cost(edge1, edge2, node1, node2)
        if edge1.is_not_eps():
            self.sedge_distortion[edge1] = edge2
            self.use_source_edge(edge1)
        if edge2.is_not_eps():
            self.tedge_distortion[edge2] = edge1
            self.use_target_node(edge2)

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
