from cfggenerator.python.cfggenerator import PythonCfgGenerator
from api.functions import *

from cfggrader.utils.graph_collapser import *
from cfggrader.utils.lsap_solver import Munkres

from cfggrader.dfs_ged import *
from cfggrader.classes.cost_function import *
from cfggrader.classes.py_cost_function import *

def check_cfggenerator():
    cfg = PythonCfgGenerator.generate_python_from_file("../datasets/segiempat/juryssolution/segiempatcontoh.py")
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
    cfg_solution = PythonCfgGenerator.generate_python_from_file("../datasets/segiempat/juryssolution/segiempatcontoh.py")
    cfg_jury = PythonCfgGenerator.generate_python_from_file("../datasets/segiempat/juryssolution/segiempatcontoh.py")

    graph_source = digraph_to_graph(cfg_solution)
    graph_target = digraph_to_graph(cfg_jury)

    # print(graph_source)
    graph_source = pygraph_to_ged_graph(graph_source)
    graph_target = pygraph_to_ged_graph(graph_target)
    print(f'size1: {len(graph_source.nodes)}, size2: {len(graph_target.nodes)}')
    # print("===========================")
    # for node in graph_source.nodes:
    #     print(node)
    #     print("=========== separate node ==========")

    dfs_ged = DFSGED(graph_source, graph_target, PyCostFunction())
    dfs_ged.init()
    print(f'GED: {dfs_ged.calculate_edit_distance()}')

test_ged()
