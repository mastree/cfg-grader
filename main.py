import math

from grader.src.api.functions import *
from grader.src.cfggenerator.cfggenerator import PythonCfgGenerator

from grader.src.ged.classes.general_cost_function import GeneralCostFunction
from grader.src.ged.utils.lsap_solver import Munkres
from grader.src.ged.dfs_ged import DFSGED


def draw_digraph(digraph, filename):
    digraph.draw(f'generatedimg/{filename}', prog='dot')


def draw_graph(src, filename):
    PythonCfgGenerator.draw_python_from_file(src, filename)


def check_graph_draw():
    PythonCfgGenerator.draw_python_from_file("./datasets/segiempat/juryssolution/segiempatcontoh.py",
                                             "generatedimg/segiempatcontoh")
    PythonCfgGenerator.draw_python_from_file("./datasets/segiempat/juryssolution/segiempatcontoh_delta.py",
                                             "generatedimg/segiempatcontoh_delta")


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


jurys = ["./datasets/segiempat/juryssolution/segiempatcontoh.py",
         "./datasets/segiempat/juryssolution/segiempatcontoh2.py",
         "./datasets/segiempat/juryssolution/segiempatcontoh_delta.py"]

solutions = ["./datasets/segiempat/solution/segiempat103.py",
             "./datasets/segiempat/solution/segiempat104.py",
             "./datasets/segiempat/solution/segiempat105.py",
             "./datasets/segiempat/solution/segiempat107.py"]


def bias_func(x):
    return math.sqrt(x)


def test_all():
    scores = []
    for jury in jurys:
        graph_target = PythonCfgGenerator.generate_python_from_file(jury)
        graph_target = compress_graph_component_id(graph_target)

        for solution in solutions:
            graph_source = PythonCfgGenerator.generate_python_from_file(solution)
            graph_source = compress_graph_component_id(graph_source)
            dfs_ged = DFSGED(graph_source, graph_target, GeneralCostFunction(False))
            # dfs_ged.set_use_node_relabel(False)

            approx_ed = dfs_ged.calculate_edit_distance(False)
            approx_normalized_ed = edit_distance_to_similarity_score(dfs_ged.get_normalized_edit_distance(), bias_func)

            approx_ed_rel = dfs_ged.calculate_edit_distance(False, True)
            approx_normalized_ed_rel = edit_distance_to_similarity_score(dfs_ged.get_normalized_edit_distance(), bias_func)

            ed = dfs_ged.calculate_edit_distance()
            normalized_ed = edit_distance_to_similarity_score(dfs_ged.get_normalized_edit_distance(), bias_func)

            # print(f'jury: {jury}')
            # print(f'solution: {solution}')
            # print(f'{normalized_ed} -> {approx_normalized_ed}')
            scores.append(normalized_ed)
            # if normalized_ed < 0.5:
            #     dfs_ged.print_matching()

            assert (normalized_ed >= approx_normalized_ed)
            # if normalized_ed != approx_normalized_ed:
            print(f'{normalized_ed} -> {approx_normalized_ed} -> {approx_normalized_ed_rel}')
            print(jury)
            print(solution)
    print(f'average: {sum(scores) / len(scores)}')


def test_ged(file1, file2):
    print(f'solution: {file1}')
    print(f'jury: {file2}')

    graph_source = PythonCfgGenerator.generate_python_from_file(file1)
    graph_target = PythonCfgGenerator.generate_python_from_file(file2)

    print(f'size1: {len(graph_source.nodes)}, size2: {len(graph_target.nodes)}')

    dfs_ged = DFSGED(graph_source, graph_target, GeneralCostFunction())
    ed = dfs_ged.calculate_edit_distance()
    normalized_ed = dfs_ged.get_normalized_edit_distance()
    print(dfs_ged.get_node_matching_string())
    print(f'GED: {ed}')
    print(f'similarity score: {1 - normalized_ed}')


def test_json():
    import json

    raw_string = ""
    with open("webservice/tests/json/grader-sample.json", "r") as f:
        raw_string = f.read()

    json_data = json.loads(raw_string)
    print(json_data)


# test_ged(solutions[0], jurys[0])
# test_ged(jurys[0], solutions[0])
test_all()
# test_json()

# draw_graph(solutions[0], "generatedimg/solution")
# draw_graph(jurys[0], "generatedimg/jury")
