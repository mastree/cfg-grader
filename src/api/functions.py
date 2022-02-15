from classes.graph import Graph
from classes.node import Node
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
    node_count = 1 # may be better to use 0-indexing (?)
    id_to_new_id = {}
    for node_id in digraph_nodes:
        id_to_new_id[node_id] = node_count

        node_label = digraph.get_node(node_id).attr['label']
        node_label = remove_number_from_label(node_label)

        out_edges = digraph.out_edges(node_id)
        for out_edge in out_edges:
            edges_to_be_added.append(out_edge)

        node = Node(int(node_count), node_label)
        graph.add_node(node)

        node_count += 1
    
    for edge in edges_to_be_added:
        try:
            graph.get_node(id_to_new_id[edge[0]]).add_adjacent(graph.get_node(id_to_new_id[edge[1]]))
        except e:
            print(e)

    return graph

def graph_to_digraph(graph: Graph):
    digraph = pgv.agraph.AGraph(directed=True)

    edges = []
    for node in graph.nodes:
        digraph.add_node(str(node.get_label()), label=node.get_info())
        for out_node in node.out_nodes:
            edges.append((str(node.get_label()), str(out_node.get_label())))

    for edge in edges:
        digraph.add_edge(edge[0], edge[1])
    
    return digraph
    