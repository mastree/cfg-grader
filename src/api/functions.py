from classes.graph import Graph
from classes.node import Node
from cfggrader.classes.graph import Graph as GEDGraph, Node as GEDNode, Edge as GEDEdge
from cfggrader.classes.graph_component import GraphComponent
import pygraphviz as pgv


def remove_number_from_label(node_label):
    pos = node_label.find(':')
    if (pos == -1):
        return node_label
    return node_label[pos + 2:]


def digraph_to_graph(digraph: pgv.agraph.AGraph):
    graph = Graph()
    digraph_nodes = digraph.nodes()

    edges_to_be_added = []
    node_count = 1  # may be better to use 0-indexing (?)
    id_to_new_id = {}
    for node_id in digraph_nodes:
        id_to_new_id[node_id] = node_count

        node_label = digraph.get_node(node_id).attr['label']
        node_label = remove_number_from_label(node_label)

        out_edges = digraph.out_edges(node_id)
        for out_edge in out_edges:
            edges_to_be_added.append(out_edge)

        node = Node(int(node_count), {"rawLine": node_label})
        graph.add_node(node)

        node_count += 1

    for edge in edges_to_be_added:
        try:
            graph.get_node(id_to_new_id[edge[0]]).add_adjacent(graph.get_node(id_to_new_id[edge[1]]))
        except e:
            print(e)

    return graph


def node_raw_info_to_str(node: Node):
    str_info = ''
    for info in node.get_info():
        if str_info == '':
            str_info += info["rawLine"]
        else:
            str_info += f'\n{info["rawLine"]}'
    return str_info


def graph_to_digraph(graph: Graph):
    digraph = pgv.agraph.AGraph(directed=True)

    edges = []
    for node in graph.nodes:
        digraph.add_node(str(node.get_label()), label=[info["rawLine"] for info in node.get_info()])
        for out_node in node.out_nodes:
            edges.append((str(node.get_label()), str(out_node.get_label())))

    for edge in edges:
        digraph.add_edge(edge[0], edge[1])

    return digraph


def pygraph_to_ged_graph(graph: Graph):
    ged_graph: GEDGraph = GEDGraph()

    # build nodes
    id_node_dict = {}
    for node in graph.get_nodes():
        ged_node = GEDNode(node.label, node.info)
        ged_graph.add_node(ged_node)
        id_node_dict[ged_node.get_id()] = ged_node

    # build edges
    for node in graph.get_nodes():
        for edge in node.get_out_nodes():
            from_node = id_node_dict[node.get_label()]
            to_node = id_node_dict[edge.get_label()]
            ged_edge = GEDEdge(from_node=from_node, to_node=to_node)
            from_node.add_edge(ged_edge)
            to_node.add_edge(ged_edge)
            ged_graph.add_edge(ged_edge)

    return ged_graph
