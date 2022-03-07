from grader.src.cfggenerator.cfggenerator import PythonCfgGenerator

from grader.src.cfggrader.classes.general_cost_function import GeneralCostFunction
from grader.src.cfggrader.utils.lsap_solver import Munkres
from grader.src.cfggrader.dfs_ged import DFSGED


def draw_digraph(digraph, filename):
    digraph.draw(f'generatedimg/{filename}', prog='dot')


def check_graph_draw():
    PythonCfgGenerator.draw_python_from_file("./datasets/segiempat/juryssolution/segiempatcontoh.py", "generatedimg/segiempatcontoh")
    PythonCfgGenerator.draw_python_from_file("./datasets/segiempat/juryssolution/segiempatcontoh_delta.py", "generatedimg/segiempatcontoh_delta")


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
    graph_source = PythonCfgGenerator.generate_python_from_file("./datasets/segiempat/juryssolution/segiempatcontoh_delta.py")
    graph_target = PythonCfgGenerator.generate_python_from_file("./datasets/segiempat/juryssolution/segiempatcontoh.py")

    print(f'size1: {len(graph_source.nodes)}, size2: {len(graph_target.nodes)}')

    dfs_ged = DFSGED(graph_source, graph_target, GeneralCostFunction(), 2000)
    print(f'GED: {dfs_ged.calculate_edit_distance()}')
    dfs_ged.print_matching()


test_ged()

