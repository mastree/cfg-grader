import copy
from typing import Callable

from grader.src.ged.classes.graph import Graph
from grader.src.ged.classes.graph_component import *


def compress_graph_component_id(graph: Graph, start_id=1) -> Graph:
    result = Graph()
    last_id = start_id - 1
    id_node = {}
    for node in graph.nodes:
        last_id += 1
        id_node[node.component_id] = Node(last_id, copy.deepcopy(node.info))
        result.add_node(id_node[node.component_id])

    for edge in graph.edges:
        last_id += 1

        from_node = id_node[edge.from_node.component_id]
        to_node = id_node[edge.to_node.component_id]

        new_edge = Edge(to_node, from_node, copy.deepcopy(edge.info))
        new_edge.set_id(last_id)

        from_node.add_edge(new_edge)
        if from_node.component_id != to_node.component_id:
            to_node.add_edge(new_edge)

        result.add_edge(new_edge)

    return result


def edit_distance_to_similarity_score(dist, func: Callable[[float], float]):
    if func is None:
        return 1 - dist
    return func(1 - dist)
