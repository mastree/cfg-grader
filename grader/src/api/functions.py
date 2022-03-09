import copy
import graphviz
from typing import Callable

from grader.src.ged.classes.graph import Graph
from grader.src.ged.classes.graph_component import *


def compress_graph_component_id(graph: Graph, start_id=1) -> Graph:
    result = Graph()
    last_id = start_id - 1
    id_node = {}
    for node in graph.nodes:
        last_id += 1
        new_node = Node(last_id, copy.deepcopy(node.info))
        id_node[node.get_id()] = new_node
        result.add_node(new_node)

    for edge in graph.edges:
        last_id += 1

        from_node = id_node[edge.from_node.get_id()]
        to_node = id_node[edge.to_node.get_id()]

        new_edge = Edge(from_node, to_node, copy.deepcopy(edge.info))
        new_edge.set_id(last_id)

        from_node.add_edge(new_edge)
        if from_node.get_id() != to_node.get_id():
            to_node.add_edge(new_edge)

        result.add_edge(new_edge)

    return result


def edit_distance_to_similarity_score(dist, func: Callable[[float], float]):
    if func is None:
        return 1 - dist
    return func(1 - dist)


def graph_to_digraph(graph: Graph) -> graphviz.Digraph:
    digraph = graphviz.Digraph()

    edges = []
    for node in graph.nodes:
        digraph.node(str(node.get_id()), label=f'{node.get_id()}: {[info["rawLine"] for info in node.info]}')
        for out_edge in node.out_edges:
            out_node = out_edge.to_node
            edges.append((str(node.get_id()), str(out_node.get_id())))

    digraph.edges(edges)
    return digraph
