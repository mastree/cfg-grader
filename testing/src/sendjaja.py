from munkres import Munkres
from pycfg.pycfg import CFGNode, PyCFG, slurp


def generate_cfg(source_code):
    CFGNode.cache = {}
    cfg = PyCFG()
    cfg.gen_cfg(source_code)
    g = CFGNode.to_graph([])
    return g


def generate_cfg_from_file(filename):
    return generate_cfg(slurp(filename).strip())


def collapse(graph):
    new_graph = graph
    nodes = graph.nodes()
    to_be_removed = []
    for i in range(len(nodes)):
        curr_out_edges = graph.out_edges(nodes[i])
        if (len(curr_out_edges) == 1 and nodes[i] not in to_be_removed):
            start_node = nodes[i]
            curr_node = nodes[i]
            (_, next_node) = curr_out_edges[0]
            node = graph.get_node(start_node)
            label = node.attr['label']
            stop = False
            while (not stop):
                if (len(graph.out_edges(next_node)) == 1 and len(graph.in_edges(next_node)) == 1):
                    curr_node = next_node
                    to_be_removed.append(curr_node)
                    node = graph.get_node(curr_node)
                    label += '\n' + node.attr['label']
                    (_, next_node) = graph.out_edges(curr_node)[0]
                elif (len(graph.out_edges(next_node)) != 1 and len(graph.in_edges(next_node)) == 1):
                    stop_node = next_node
                    to_be_removed.append(next_node)
                    node = graph.get_node(next_node)
                    label += '\n' + node.attr['label']
                    stop = True
                else:
                    stop_node = curr_node
                    stop = True

            if (start_node != stop_node):
                if (len(graph.out_edges(stop_node)) > 0):
                    edges = graph.out_edges(stop_node)
                    for edge in edges:
                        (_, end_node) = edge
                        new_graph.add_edge(start_node, end_node)
                node = new_graph.get_node(start_node)
                node.attr['label'] = label

    if (len(to_be_removed) > 0):
        removed_edges = []
        [removed_edges.append(x) for x in new_graph.edges(to_be_removed) if x not in removed_edges]
        new_graph.remove_edges_from(removed_edges)
        new_graph.remove_nodes_from(to_be_removed)

    return new_graph


def create_sendjaja_graph(source):
    return collapse(generate_cfg(source))


def create_cost_matrix(graph1, graph2):
    nodes1 = graph1.nodes()
    nodes2 = graph2.nodes()
    cost_matrix = [[0 for col in range(len(nodes1) + len(nodes2))] for row in range(len(nodes1) + len(nodes2))]

    # Fill section 1 (real node to real node)
    for i in range(len(nodes1)):
        for j in range(len(nodes2)):
            in1 = len(graph1.in_neighbors(nodes1[i]))
            in2 = len(graph2.in_neighbors(nodes2[j]))
            out1 = len(graph1.out_neighbors(nodes1[i]))
            out2 = len(graph2.out_neighbors(nodes2[j]))
            cost_matrix[i][j] = (out1 + out2 - (2 * min(out1, out2))) + (in1 + in2 - (2 * min(in1, in2)))

    # Fill section 2 (delete node in graph 1)
    for i in range(len(nodes1)):
        for j in range(len(nodes1)):
            if (i == j):
                oe = len(graph1.out_edges(nodes1[i]))
                ie = len(graph1.in_edges(nodes1[i]))
                cost_matrix[i][len(nodes2) + j] = 1 + oe + ie
            else:
                cost_matrix[i][len(nodes2) + j] = 999

    # Fill section 3 (delete node in graph 2)
    for i in range(len(nodes2)):
        for j in range(len(nodes2)):
            if (i == j):
                oe = len(graph2.out_edges(nodes2[i]))
                ie = len(graph2.in_edges(nodes2[i]))
                cost_matrix[len(nodes1) + i][j] = 1 + oe + ie
            else:
                cost_matrix[len(nodes1) + i][j] = 999

    return cost_matrix


def compare(g1, g2):
    m = Munkres()
    cost_matrix = create_cost_matrix(g1, g2)
    indexes = m.compute(cost_matrix)
    total = 0
    details = []
    for row, column in indexes:
        value = cost_matrix[row][column]
        total += value
        details.append([row, column, value])

    final_score = (1 - (total / (len(g1.nodes()) + len(g2.nodes()) + len(g1.edges()) +len(g2.edges())))) * 100
    final_score = max(final_score, 0)
    return final_score, total, details
