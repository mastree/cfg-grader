from cfggenerator.python.cfggenerator import PythonCfgGenerator
from api.functions import *

from cfggrader.utils.graph_collapser import *
from cfggrader.utils.lsap_solver import Munkres

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
    lsap_solver = Munkres()

    cost_matrix = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4],
    ]

    costs, starred_indices = lsap_solver.compute(cost_matrix)
    print(f'costs: {costs}')
    print(starred_indices)

    starred_indices.sort(key=lambda x: cost_matrix[x[0]][x[1]])
    print(starred_indices)

check_munkres()
