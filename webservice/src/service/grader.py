import copy

from grader.src.ged.classes.graph import Graph
from grader.src.ged.classes.graph_component import Node, Edge
from grader.src.grader import grade
from webservice.src.model.grader_request import GraderRequest
from webservice.src.model.graph_view import GraphView


def graph_view_to_graph(graph_view: GraphView) -> Graph:
    graph = Graph()
    id_node = {}

    for node_view in graph_view.nodes:
        info = []
        if isinstance(node_view.info, list):
            info = copy.deepcopy(node_view.info)

        node = Node(node_view.id, info)
        id_node[node.get_id()] = node
        graph.add_node(node)

    for edge_view in graph_view.edges:
        info = []
        if isinstance(edge_view.info, list):
            info = copy.deepcopy(edge_view.info)

        from_node = id_node[edge_view.from_node]
        to_node = id_node[edge_view.to_node]

        edge = Edge(to_node, from_node, info)
        from_node.add_edge(edge)
        if from_node.get_id() != to_node:
            to_node.add_edge(edge)

        graph.add_edge(edge)

    return graph


def get_scores(grader_request: GraderRequest) -> tuple[int, int, int]:
    graph_source = graph_view_to_graph(grader_request.solution)
    graph_targets: list[Graph] = []

    for jury_solution in grader_request.jury_solutions:
        graph_targets.append(graph_view_to_graph(jury_solution))

    scores = grade(graph_source, graph_targets)
    max_score = max(scores)
    min_score = min(scores)
    avg_score = sum(scores) / len(scores)

    return max_score, min_score, avg_score
