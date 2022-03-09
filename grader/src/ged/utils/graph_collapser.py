import copy

from grader.src.api.functions import *

from grader.src.ged.utils.dsu import CollapserDSU
from grader.src.ged.classes.graph import Graph
from grader.src.ged.classes.graph_component import *


"""
Note: Graph collapsing would not preserve information in edges that were collapsed
"""
def collapse(input_graph: Graph):
    input_graph = compress_graph_component_id(input_graph)
    nodes = input_graph.nodes
    edges = input_graph.edges
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

    graph = Graph()
    id_node = {}
    for node in nodes:
        if node.get_id() == dsu.find_par(node.get_id()):
            new_node = Node(node.get_id(), dsu.info[node.get_id()])
            graph.add_node(new_node)
            id_node[new_node.get_id()] = new_node

    for edge in edges:
        new_from_id = dsu.find_par(edge.from_node.get_id())
        new_to_id = dsu.find_par(edge.to_node.get_id())

        if new_from_id != new_to_id or edge.from_node.get_id() == edge.to_node.get_id():
            from_node = id_node[new_from_id]
            to_node = id_node[new_to_id]
            new_edge = Edge(from_node, to_node, copy.deepcopy(edge.info))

            from_node.add_edge(new_edge)
            if from_node.get_id() != to_node.get_id():
                to_node.add_edge(new_edge)

            graph.add_edge(new_edge)

    return compress_graph_component_id(graph)


def uncollapse(input_graph: Graph):
    input_graph = compress_graph_component_id(input_graph)
    graph = Graph()
    last_id = 0
    input_size = len(input_graph.nodes) + 1
    id_nodes = [[] for i in range(input_size)]
    for input_node in input_graph.nodes:
        for input_info in input_node.info:
            last_id += 1
            node = Node(last_id, [copy.deepcopy(input_info)])
            id_nodes[input_node.get_id()].append(node)
            graph.add_node(node)

    for input_edge in input_graph.edges:
        input_from_id = input_edge.from_node.get_id()
        input_to_id = input_edge.to_node.get_id()

        from_node = id_nodes[input_from_id][-1]
        to_node = id_nodes[input_to_id][0]
        last_id += 1

        edge = Edge(from_node, to_node, copy.deepcopy(input_edge.info))
        edge.set_id(last_id)

        from_node.add_edge(edge)
        if from_node.get_id != to_node.get_id:
            to_node.add_edge(edge)

        graph.add_edge(edge)

    for nodes in id_nodes:
        from_node = None
        for to_node in nodes:
            if from_node is not None:
                last_id += 1
                edge = Edge(from_node, to_node)
                edge.set_id(last_id)

                from_node.add_edge(edge)
                if from_node.get_id != to_node.get_id:
                    to_node.add_edge(edge)

                graph.add_edge(edge)
            from_node = to_node

    return graph
