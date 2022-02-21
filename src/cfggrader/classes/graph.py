from cfggrader.classes.graph_component import *
import copy


class Graph:
    def __init__(self):
        self.nodes: list[Node] = []
        self.edges = list[Edge] = []
        self.id = string = ''

    def set_nodes(self, nodes: list):
        self.nodes = nodes

    def set_edges(self, edges: list):
        self.edges = edges

    def set_id(self, graph_id):
        self.id = graph_id

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def find_node_with_id(self, id: int):
        for node in self.nodes:
            if (node.component_id == id):
                return node
