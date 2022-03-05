from grader.src.cfggenerator.cfggenerator import PythonCfgGenerator
from grader.src.api.functions import *

from grader.src.cfggrader.classes.general_cost_function import GeneralCostFunction
from grader.src.cfggrader.utils.lsap_solver import Munkres
from grader.src.cfggrader.utils.graph_collapser import collapse
from grader.src.cfggrader.dfs_ged import DFSGED


def draw_graph(digraph, filename):
    digraph.draw(f'generatedimg/{filename}', prog='dot')

def check_cfggenerator():
    cfg = PythonCfgGenerator.generate_python_from_file("./datasets/segiempat/juryssolution/segiempatcontoh.py")
    # print(cfg)

    graph = digraph_to_graph(cfg)
    cgraph = collapse(graph)

    digraph = graph_to_digraph(graph)
    digraph.draw('generatedimg/digraph2.png', prog='dot')

    cdigraph = graph_to_digraph(cgraph)
    cdigraph.draw('generatedimg/digraph_collapsed2.png', prog='dot')

    # print(cgraph)
    # print(digraph)
    # print("====================================")
    # print(cdigraph)

def check_graph_draw():
    cfg = PythonCfgGenerator.generate_python_from_file("./datasets/segiempat/juryssolution/segiempatcontoh.py")
    draw_graph(cfg, "test_draw.png")

def check_munkres():
    cost_matrix = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4],
    ]
    munkres = Munkres()

    costs = munkres.compute(cost_matrix)
    starred_indices = munkres.get_starred_indices()
    print(f'costs: {costs}')
    print(starred_indices)

    starred_indices.sort(key=lambda x: cost_matrix[x[0]][x[1]])
    print(starred_indices)

def test_ged():
    # cfg_solution = PythonCfgGenerator.generate_python_from_file("../datasets/segiempat/solution/segiempat103.py")
    cfg_solution = PythonCfgGenerator.generate_python_from_file("./datasets/segiempat/juryssolution/segiempatcontoh_delta.py")
    cfg_jury = PythonCfgGenerator.generate_python_from_file("./datasets/segiempat/juryssolution/segiempatcontoh.py")

    draw_graph(cfg_solution, "test_solution.png")
    draw_graph(cfg_jury, "test_jury.png")

    graph_source = digraph_to_graph(cfg_solution)
    graph_target = digraph_to_graph(cfg_jury)

    # cfg_solution = graph_to_digraph(graph_source)
    # cfg_jury = graph_to_digraph(graph_target)
    # draw_graph(cfg_solution, "test_solution.png")
    # draw_graph(cfg_jury, "test_jury.png")


    # print(graph_source)
    graph_source = pygraph_to_ged_graph(graph_source)
    graph_target = pygraph_to_ged_graph(graph_target)
    print(f'size1: {len(graph_source.nodes)}, size2: {len(graph_target.nodes)}')
    # print("===========================")
    # for node in graph_source.nodes:
    #     print(node)
    #     print("=========== separate node ==========")

    dfs_ged = DFSGED(graph_source, graph_target, GeneralCostFunction())
    print(f'GED: {dfs_ged.calculate_edit_distance()}')
    dfs_ged.print_matching()

test_ged()
