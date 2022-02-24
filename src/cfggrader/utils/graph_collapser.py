from cfggrader.utils.dsu import DSU
from classes.graph import Graph


def collapse(input_graph: Graph):
    g = input_graph.get_clone()
    nodes = g.get_nodes()
    dsu = DSU(len(nodes))

    # Merge nodes with the same flow
    for node in nodes:
        out_nodes = node.get_out_nodes()
        if len(out_nodes) > 1:
            continue
        label = node.get_label()
        for out_node in out_nodes:
            adj_label = out_node.get_label()
            if len(out_node.get_in_nodes()) <= 1:
                dsu.merge(label, adj_label)

    # Merge infos to parent node
    for node in nodes:
        label = node.get_label()
        par_label = dsu.find_par(label)
        if (label != par_label):
            continue
        cur_out_nodes = node.get_out_nodes()
        if (len(cur_out_nodes) == 1):
            cur_node = cur_out_nodes[0]
            while (dsu.check_same(cur_node.get_label(), par_label)):
                for info in cur_node.get_info():
                    node.add_info(info)
                cur_out_nodes = cur_node.get_out_nodes()
                if (len(cur_out_nodes) == 1):
                    cur_node = cur_out_nodes[0]
                else:
                    break

    # Create new adjacency list
    new_adj = {}
    for node in nodes:
        label = node.get_label()
        par_label = dsu.find_par(label)
        if (par_label not in new_adj):
            new_adj[par_label] = set()
        for adj_node in node.get_out_nodes():
            adj_label = adj_node.get_label()
            par_adj_label = dsu.find_par(adj_label)
            if (adj_label == par_adj_label):
                new_adj[par_label].add(adj_label)

    # Reset out and in nodes list for every node
    for node in nodes:
        node.set_out_nodes([])
        node.set_in_nodes([])

    # Get new nodes and add new adjacent for every node
    new_nodes = []
    for node in nodes:
        label = node.get_label()
        par_label = dsu.find_par(label)
        if label != par_label:
            continue
        new_nodes.append(node)
        if label in new_adj:
            for adj_label in new_adj[label]:
                node.add_adjacent(g.get_node(adj_label))

    # Relabel Node
    for idx, node in enumerate(new_nodes):
        node.set_label(idx + 1)

    # Set new node to graph
    g.set_nodes(new_nodes)
    return g
