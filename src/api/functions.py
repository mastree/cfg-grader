from classes.graph import Graph
import pygraphviz as pgv

def digraph_to_graph(digraph: pgv.AGraph):
    # ret = Graph()
    # for node in graph.
    # print(digraph)
    # print(digraph.nodes())
    # print(digraph.get)
    # for node in digraph.nodes:
    #     print(type(node))
    digraph_nodes = digraph.nodes()
    print(digraph_nodes)
    