from grader.src.cfggenerator.cfggenerator import PythonCfgGenerator

from grader.src.cfggrader.classes.general_cost_function import GeneralCostFunction
from grader.src.cfggrader.utils.lsap_solver import Munkres
from grader.src.cfggrader.dfs_ged import DFSGED


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


def test_all():
    scores = []
    for jury in jurys:
        graph_target = PythonCfgGenerator.generate_python_from_file(jury)

        for solution in solutions:
            graph_source = PythonCfgGenerator.generate_python_from_file(solution)
            dfs_ged = DFSGED(graph_source, graph_target, GeneralCostFunction())
            dfs_ged.set_use_node_relabel(False)

            approx_ed = dfs_ged.calculate_edit_distance(False)
            approx_normalized_ed = 1 - dfs_ged.get_normalized_edit_distance()

            approx_ed_rel = dfs_ged.calculate_edit_distance(False, True)
            approx_normalized_ed_rel = 1 - dfs_ged.get_normalized_edit_distance()

            ed = dfs_ged.calculate_edit_distance()
            normalized_ed = 1 - dfs_ged.get_normalized_edit_distance()

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
    dfs_ged.print_matching()
    print(f'GED: {ed}')
    print(f'similarity score: {1 - normalized_ed}')


# test_ged(solutions[0], jurys[0])
# test_ged(jurys[0], solutions[0])
test_all()

# draw_graph(solutions[0], "generatedimg/solution")
# draw_graph(jurys[0], "generatedimg/jury")
