import os.path

from notal.intermediate.src.classes.graph import Graph

from grader.src.ged.classes.graph import Graph as GGraph
from grader.src.ged.classes.graph_component import Node as GNode, Edge as GEdge
from notal.cfg_generator.src.api.functions import get_cfg


def graph_to_grader_graph(graph: Graph):
    ggraph = GGraph()
    node_id = {}
    id_gnode = {}
    last_id = 0
    for node in graph.nodes:
        last_id += 1
        node_id[node] = last_id
        gnode = GNode(last_id, [{'label': info} for info in node.info])
        id_gnode[last_id] = gnode
        ggraph.add_node(gnode)

    for source in graph.nodes:
        source_id = node_id[source]
        for target in source.adjacent:
            target_id = node_id[target]
            last_id += 1

            gsource = id_gnode[source_id]
            gtarget = id_gnode[target_id]
            gedge = GEdge(last_id, gsource, gtarget)
            gsource.add_edge(gedge)
            gtarget.add_edge(gedge)
            ggraph.add_edge(gedge)
    return ggraph
