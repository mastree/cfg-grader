from grader.src.ged.classes.graph_component import *


class Graph:
    def __init__(self):
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.id: str = ''

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

    def find_node_with_id(self, search_id: int):
        for node in self.nodes:
            if node.component_id == search_id:
                return node
        return None

    def __str__(self):
        ret = ""
        for node in self.nodes:
            ret += f'{node}\n'
        return ret
