class GraphComponent:
    def __init__(self, component_id=None, info=[]):
        self.component_id: int = component_id
        self.info: list[dict] = info

    def set_info(self, info):
        self.info = info

    def get_info(self):
        return self.info

    def get_id(self):
        return self.component_id

    def is_eps(self):
        return self.component_id is None

    def is_not_eps(self):
        return self.component_id is not None


class Node(GraphComponent):
    def __init__(self, component_id=None, info=[]):
        super().__init__(component_id, info)
        self.edges: list[Edge] = []

    def get_edges(self):
        return self.edges

    def set_edges(self, edges: list):
        self.edges = edges

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_edge_to(self, node):
        for edge in self.edges:
            if node.component_id == edge.to_node.component_id:
                return edge
        return None

    def __str__(self):
        edges = []
        for edge in self.edges:
            edges.append(f'{edge.component_id : <3}: {(edge.from_node.component_id, edge.to_node.component_id)}')
        ret = f'{self.component_id : <3} label: {self.info}\n{"edges:" : <7} {edges}'
        return ret


class Edge(GraphComponent):
    def __init__(self, info=[], from_node=None, to_node=None):
        super().__init__()
        self.set_info(info)
        self.from_node: Node = from_node
        self.to_node: Node = to_node

    def set_id(self, component_id):
        self.component_id = component_id

    def set_from_node(self, from_node):
        self.from_node = from_node

    def set_to_node(self, to_node):
        self.to_node = to_node

    def get_from_node(self):
        return self.from_node

    def get_to_node(self):
        return self.to_node

    def get_other_end(self, node: Node):
        if node.component_id == self.from_node.component_id:
            return self.to_node
        return self.from_node
