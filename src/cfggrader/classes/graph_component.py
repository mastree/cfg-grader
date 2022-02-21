class GraphComponent:
    def __init__(self, component_id=None, info={}):
        self.component_id: int = component_id
        self.info: dict = info

    def set_info(self, info):
        self.info = info

    def get_info(self):
        return self.info

    def get_id(self):
        return self.component_id


class Node(GraphComponent):
    def __init__(self, component_id=None, info={}):
        self(component_id, info)
        self.edges: list[Edge] = []

    def get_edges(self):
        return self.edges

    def set_edges(self, edges: list):
        self.edges = edges

    def add_edge(self, edge):
        self.edges.append(edge)


class Edge(GraphComponent):
    def __init__(self, info={}, from_node=None, to_node=None):
        self()
        self.set_info(info)
        self.from_node: Node = from_node
        self.to_node: Node = to_node

    def set_from_node(self, from_node):
        self.from_node = from_node

    def set_to_node(self, to_node):
        self.to_node = to_node

    def get_from_node(self):
        return self.from_node

    def set_to_node(self):
        return self.to_node
