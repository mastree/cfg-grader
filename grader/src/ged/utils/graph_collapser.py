import copy
from collections import deque

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


def __flood_fill(graph: Graph, root: Node, parent: Node) -> set:
    ret = set()
    q = deque()
    q.append(root)
    ret.add(root.get_id())
    ret.add(parent.get_id())

    while len(q) > 0:
        node = q.popleft()
        for edge in node.out_edges:
            nnode = edge.to_node
            if nnode.get_id() in ret:
                continue
            q.append(nnode)
            ret.add(nnode.get_id())

    return ret


"""
Propagate branching on if statement
"""
def propagate_branching(input_graph: Graph, node_key: str = "label"):
    graph = collapse(input_graph)
    last_id = 0
    for node in graph.nodes:
        new_info = []
        for info in node.info:
            new_info.append({ikey: info[ikey] for ikey in info if ikey == node_key})
        node.set_info(new_info)
        last_id = max(last_id, node.get_id())
        for edge in node.out_edges:
            last_id = max(last_id, edge.get_id())

    snode = len(graph.nodes)
    for i in range(snode):
        erase_nodes = []
        for node in graph.nodes:
            if not (len(node.in_edges) == 1 and len(node.out_edges) > 1):
                continue

            parent = node.in_edges[0].from_node
            parent_last = parent.info[-1][node_key]
            last = node.info[-1][node_key]
            if last != parent_last or node.get_id() == parent.get_id():
                continue

            # Handle Diamond Branching
            vis_counter = {}
            for edge in node.out_edges:
                onode = edge.to_node
                vis = __flood_fill(graph, onode, node)
                for x in vis:
                    if x not in vis_counter:
                        vis_counter[x] = 0
                    vis_counter[x] += 1

            erase_edges = []
            new_edges = []
            for edge in node.out_edges:
                onode = edge.to_node
                if vis_counter[onode.get_id()] <= 1:
                    continue

                last_id += 1
                new_node = Node(last_id)
                last_id += 1
                new_edge = Edge(node, new_node)
                new_edge.set_id(last_id)
                last_id += 1
                new_oedge = Edge(new_node, onode)
                new_oedge.set_id(last_id)

                new_edges.append(new_edge)
                new_node.add_edge(new_edge)
                new_node.add_edge(new_oedge)
                onode.add_edge(new_oedge)

                graph.add_node(new_node)
                graph.add_edge(new_edge)
                graph.add_edge(new_oedge)

                erase_edges.append(edge)

            for new_edge in new_edges:
                node.add_edge(new_edge)

            for erase_edge in erase_edges:
                edge_id = erase_edge.get_id()
                graph.erase_edge(edge_id)
                erase_edge.from_node.erase_edge(edge_id)
                erase_edge.to_node.erase_edge(edge_id)
            # End of Transformation (Diamond Branching Handling)

            for edge in node.out_edges:
                onode = edge.to_node
                new_oinfo = copy.deepcopy(node.info[:-1])
                for oinfo in onode.info:
                    new_oinfo.append(oinfo)
                onode.set_info(new_oinfo)
                new_edge = Edge(parent, onode)
                last_id += 1
                new_edge.set_id(last_id)
                parent.add_edge(new_edge)
                onode.add_edge(new_edge)
                graph.add_edge(new_edge)
            erase_nodes.append(node)

        for erase_node in erase_nodes:
            graph.erase_node(erase_node.get_id())

    # Erase Redundant Nodes
    erase_nodes = []
    for node in graph.nodes:
        if len(node.edges) == 2 and len(node.out_edges) == 1 and len(node.in_edges) == 1 and len(node.info) == 0:
            erase_nodes.append(node)

    for erase_node in erase_nodes:
        parent = node.in_edges[0].from_node
        child = node.out_edges[0].to_node
        last_id += 1
        new_edge = Edge(parent, child)
        new_edge.set_id(last_id)

        parent.add_edge(new_edge)
        child.add_edge(new_edge)
        graph.add_edge(new_edge)

        graph.erase_node(erase_node.get_id())

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
