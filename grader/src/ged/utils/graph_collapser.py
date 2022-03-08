import copy

from grader.src.api.functions import *

from grader.src.ged.utils.dsu import CollapserDSU
from grader.src.ged.classes.graph import Graph
from grader.src.ged.classes.graph_component import *


"""
Note: Graph collapsing would not preserve information in edges that were collapsed
"""
def collapse(input_graph: Graph):
    graph = compress_graph_component_id(input_graph)
    nodes = graph.nodes
    edges = graph.edges
    dsu = CollapserDSU(nodes)

    # Merge nodes with the same flow
    for node in nodes:
        out_edges = node.get_out_edges()
        if len(out_edges) > 1:
            continue

        id = node.get_id()
        for out_edge in out_edges:
            out_node = out_edge.to_node
            adj_id = out_node.get_id()
            if len(out_node.get_in_edges()) <= 1:
                dsu.merge(id, adj_id)

    new_graph = Graph()
    id_node = {}
    for node in nodes:
        if node.get_id() == dsu.find_par(node.get_id()):
            new_node = node.clone_node_only()
            new_graph.add_edge(new_node)
            id_node[new_node.get_id()] = new_node

    for edge in edges:
        new_from_id = dsu.find_par(edge.from_node.get_id())
        new_to_id = dsu.find_par(edge.to_node.get_id())

        if new_from_id != new_to_id or edge.from_node.get_id() == edge.to_node.get_id():
            from_node = id_node[new_from_id]
            to_node = id_node[new_to_id]
            new_edge = Edge(to_node, from_node, copy.deepcopy(edge.info))

            from_node.add_edge(new_edge)
            if from_node.component_id != to_node.component_id:
                to_node.add_edge(new_edge)

            new_graph.add_edge(new_edge)

    return compress_graph_component_id(new_graph)
