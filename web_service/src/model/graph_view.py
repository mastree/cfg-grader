class NodeView:
    def __init__(self, id, info):
        self.id: int = id
        self.info: list[dict] = info


class EdgeView:
    def __init__(self, from_node, to_node, info=[]):
        self.from_node: int = from_node
        self.to_node: int = to_node
        self.info: list[dict] = info


class GraphView:
    def __init__(self, nodes=[], edges=[]):
        self.nodes: list[NodeView] = []
        self.edges: list[EdgeView] = []

        for node in nodes:
            self.nodes.append(NodeView(**node))

        for edge in edges:
            self.edges.append(EdgeView(**edge))
