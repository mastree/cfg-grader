import copy

from grader.src.ged.classes.graph import Graph
from grader.src.ged.classes.graph_component import Node, Edge
from grader.src.grader import grade
from webservice.src.model.grader_request import GraderRequest
from webservice.src.model.grader_response_data import GraderResponseData
from webservice.src.model.grading_method import GradingMethod
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

        edge = Edge(from_node, to_node, info)
        from_node.add_edge(edge)
        if from_node.get_id() != to_node:
            to_node.add_edge(edge)

        graph.add_edge(edge)

    return graph


def get_scores(grader_request: GraderRequest) -> tuple[int, int, int]:
    graph_source = graph_view_to_graph(grader_request.solution)
    graph_targets: list[Graph] = []
    time_limit = grader_request.time_limit
    time_limit_per_unit = grader_request.time_limit_per_unit
    grading_method = grader_request.grading_method

    for reference in grader_request.references:
        graph_targets.append(graph_view_to_graph(reference))

    scores, errors, feedback = grade(graph_source, graph_targets, time_limit, time_limit_per_unit)
    score = 0
    if len(scores) > 0:
        if grading_method == GradingMethod.AVERAGE:
            score = sum(scores) / len(scores)
        elif grading_method == GradingMethod.MINIMUM:
            score = min(scores)
        else:
            score = max(scores)

    return GraderResponseData(score, feedback)
