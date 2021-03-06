import math

from grader.src.api.functions import *
from grader.src.cfggenerator.cfggenerator import PythonCfgGenerator

from grader.src.ged.classes.general_cost_function import GeneralCostFunction, RelabelMethod
from grader.src.ged.utils.graph_collapser import uncollapse, collapse, propagate_branching
from grader.src.ged.utils.lsap_solver import Munkres
from grader.src.ged.dfs_ged import DFSGED
from web_service.src.model.source_grader_request import SourceGraderRequest
from web_service.src.service.source_grader import SourceGraderService, get_score

python_cfg_generator = PythonCfgGenerator()

def draw_graph(src, filename):
    python_cfg_generator.draw_python_from_file(src, f"generatedimg/{filename}")


def check_graph_draw():
    python_cfg_generator.draw_python_from_file("./datasets/segiempat/juryssolution/segiempatcontoh.py",
                                             "generatedimg/segiempatcontoh")
    python_cfg_generator.draw_python_from_file("./datasets/segiempat/juryssolution/segiempatcontoh_delta.py",
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


test_src = "./datasets/segiempat/juryssolution/test2.py"

references = ["./datasets/segiempat/juryssolution/segiempatcontoh.py",
         "./datasets/segiempat/juryssolution/segiempatcontoh2.py",
         "./datasets/segiempat/juryssolution/segiempatcontoh_delta.py"]

solutions = ["./datasets/segiempat/solution/segiempat103.py",
             "./datasets/segiempat/solution/segiempat104.py",
             "./datasets/segiempat/solution/segiempat105.py",
             "./datasets/segiempat/solution/segiempat107.py"]


def check_digraph():
    cfg = python_cfg_generator.generate_python_from_file(references[0])
    digraph = graph_to_digraph(cfg)
    digraph.render(filename="generatedimg/something", format="jpg")


def bias_func(x):
    return math.sqrt(x)


def test_all(graph_collapsed: bool = True, print_result = False):
    scores = []
    mx = 0
    for reference in references:
        graph_target = python_cfg_generator.generate_python_from_file(reference)
        if graph_collapsed:
            graph_target = propagate_branching(graph_target)
        else:
            graph_target = uncollapse(graph_target)

        for solution in solutions:
            graph_source = python_cfg_generator.generate_python_from_file(solution)
            if graph_collapsed:
                graph_source = propagate_branching(graph_source)
            else:
                graph_source = uncollapse(graph_source)

            dfs_ged = DFSGED(graph_source, graph_target, GeneralCostFunction(relabel_method=RelabelMethod.BOOLEAN_COUNT), time_limit=5000)

            approx_ed = dfs_ged.compute_edit_distance(False)
            approx_normalized_ed = dfs_ged.get_similarity_score()

            # approx_ed_rel = dfs_ged.calculate_edit_distance(False, True)
            # approx_normalized_ed_rel = dfs_ged.get_similarity_score(bias_func)
            dfs_ged.reset()

            ed = dfs_ged.compute_edit_distance()
            normalized_ed = dfs_ged.get_similarity_score()

            scores.append(normalized_ed)
            mx = max(mx, normalized_ed)
            if print_result:
                print(f'{reference.split("/")[-1]} {solution.split("/")[-1]}')
                print(f'optimal? {dfs_ged.is_solution_optimal}\nvalid: {dfs_ged.is_valid_exact_computation()}\nexact: {normalized_ed}\napprox: {approx_normalized_ed}\n')

    print(f'average: {sum(scores) / len(scores)}, max: {mx}')


def test_approximate_all(graph_collapsed: bool = True, print_result = False):
    scores = []
    mx = 0
    for reference in references:
        graph_target = python_cfg_generator.generate_python_from_file(reference)
        if graph_collapsed:
            graph_target = propagate_branching(graph_target)
        else:
            graph_target = uncollapse(graph_target)

        for solution in solutions:
            graph_source = python_cfg_generator.generate_python_from_file(solution)
            if graph_collapsed:
                graph_source = propagate_branching(graph_source)
            else:
                graph_source = uncollapse(graph_source)

            dfs_ged = DFSGED(graph_source, graph_target, GeneralCostFunction(), time_limit=3000)
            ed = dfs_ged.compute_edit_distance(False)
            normalized_ed = dfs_ged.get_similarity_score()

            scores.append(normalized_ed)
            mx = max(mx, normalized_ed)
            if print_result:
                print(f'{reference.split("/")[-1]} {solution.split("/")[-1]}')
                print(f'GED: {ed}, score: {normalized_ed}')

    print(f'average: {sum(scores) / len(scores)}, max: {mx}')


def test_ged(file1, file2, graph_collapsed=True):
    print(f'sol: {file1.split("/")[-1]}, reference: {file2.split("/")[-1]}')

    graph_source = python_cfg_generator.generate_python_from_file(file1)
    graph_target = python_cfg_generator.generate_python_from_file(file2)
    if graph_collapsed:
        graph_source = propagate_branching(graph_source)
        graph_target = propagate_branching(graph_target)
    else:
        graph_source = uncollapse(graph_source)
        graph_target = uncollapse(graph_target)

    print(f'size1: {len(graph_source.nodes)}, size2: {len(graph_target.nodes)}')

    dfs_ged = DFSGED(graph_source, graph_target, GeneralCostFunction(), time_limit=1000)
    ed = dfs_ged.compute_edit_distance()
    normalized_score = dfs_ged.get_similarity_score()
    print(dfs_ged.get_string_node_map())
    print(f'GED: {ed}')
    print(f'optimal? {dfs_ged.__is_solution_optimal}')
    print(f'similarity score: {normalized_score}')


def test_json():
    import json

    raw_string = ""
    with open("webservice/tests/json/grader-sample.json", "r") as f:
        raw_string = f.read()

    json_data = json.loads(raw_string)
    print(json_data)


def test_draw_preprocessed_cfg(src):
    try:
        cfg = python_cfg_generator.generate_python_from_file(src)
        # cfg = collapse(cfg)
        cfg = propagate_branching(cfg)
        digraph = graph_to_digraph(cfg, node_key="label")
        # digraph.render(filename="generatedimg/something_original", format="jpg")
        digraph.render(filename="generatedimg/something", format="jpg")
    except Exception as e:
        print(e)


def __read_file(filename):
    with open(filename, 'r') as file:
        raw = file.read()
        return raw


def __read_files(filenames):
    ret = []
    for filename in filenames:
        ret.append(__read_file(filename))
    return ret


def draw_report_resources(srcs):
    try:
        for src in srcs:
            cfg = python_cfg_generator.generate_python_from_file(src)
            digraph = graph_to_digraph(cfg, node_key="label")
            digraph.render(filename=f"generatedimg/{src.split('/')[-1][:-3]}", format="jpg")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    test_all(True, print_result=True)

    # req = {
    #     "references": [
    #         "ZGVmIG1heF8zKGEsIGIsIGMpOgogICAgaWYgYSA+PSBiIGFuZCBhID49IGM6CiAgICAgICAgcmV0dXJuIGEKICAgIGVsaWYgYiA+PSBhIGFuZCBiID49IGM6CiAgICAgICAgcmV0dXJuIGIKICAgIGVsc2U6CiAgICAgICAgcmV0dXJuIGMKCgo="
    #     ],
    #     "solution": "ZGVmIG1heF8zXzEoYSwgYiwgYyk6CiAgICBpZiBhID4gYiBhbmQgYSA+IGM6CiAgICAgICAgcmV0dXJuIGEKICAgIGVsaWYgYiA+IGEgYW5kIGIgPiBjOgogICAgICAgIHJldHVybiBiCiAgICBlbHNlOgogICAgICAgIHJldHVybiBjCgo=",
    #     "referencesFileNames": [
    #         "max_3.py"
    #     ],
    #     "solutionFileName": "max_3_1.py",
    #     "timeLimit": 10000
    # }
    # print(get_score(SourceGraderRequest(**req)).__dict__)
    #
    # req = {
    #     "references": [
    #         "UFJPR1JBTSBkZW1vXzEKCktBTVVTCiAgICBzdW0sIGksIG46IGludGVnZXIKCiAgICBmdW5jdGlvbiBwYW5na2F0KGEsIG46IGludGVnZXIpIC0+IGludGVnZXIKCkFMR09SSVRNQQogICAgaW5wdXQobikKICAgIGkgPC0gMQogICAgc3VtIDwtIDAKCiAgICByZXBlYXQKICAgICAgICBzdW0gPC0gc3VtICsgcGFuZ2thdCgyLCBpKQogICAgICAgIGkgPC0gaSArIDEKICAgIHVudGlsIChpID0gbikKCiAgICBvdXRwdXQoc3VtKQoKZnVuY3Rpb24gcGFuZ2thdChhLCBuOiBpbnRlZ2VyKSAtPiBpbnRlZ2VyCgpLQU1VUyBMT0tBTAogICAgcmVzLCBpOiBpbnRlZ2VyCgpBTEdPUklUTUEKICAgIHJlcyA8LSAxCiAgICByZXBlYXQgbiB0aW1lcwogICAgICAgIHJlcyA8LSByZXMgKiBhCiAgICAtPiByZXMK",
    #         "eyBNZW5naGFzaWxrYW4gMSEgKyAyISArIDMhICsgLi4uICsgbiEgfQpQUk9HUkFNIHN1bV9vZl9mYWN0b3JpYWwKS0FNVVMKICAgIG4sIGksIGo6IGludGVnZXIKICAgIHN1bSwgZmFrdG9yaWFsOiBpbnRlZ2VyCkFMR09SSVRNQQogICAgaW5wdXQobikKICAgIGkgPC0gMQogICAgc3VtIDwtIDAKICAgIHdoaWxlIChpIDw9IG4pIGRvCiAgICAgICAgaiA8LSAxCiAgICAgICAgZmFrdG9yaWFsIDwtIDEKICAgICAgICByZXBlYXQKICAgICAgICAgICAgZmFrdG9yaWFsIDwtIGZha3RvcmlhbCAqIGoKICAgICAgICAgICAgaiA8LSBqICsgMQogICAgICAgIHVudGlsIChqID0gaSkKICAgICAgICBzdW0gPC0gc3VtICsgZmFrdG9yaWFsCiAgICAgICAgaSA8LSBpICsgMQogICAgb3V0cHV0KHN1bSk="
    #     ],
    #     "solution": "UFJPR1JBTSByZXBlYXRfdW50aWwKS0FNVVMKIGksIGosIG46IGludGVnZXIKCkFMR09SSVRNQQogaW5wdXQobikKIGkgPC0gMQogcmVwZWF0CiAgaiA8LSAxCiAgcmVwZWF0CiAgIGlmIChqIG1vZCAyID0gMSkgdGhlbgogICAgb3V0cHV0KCcqJykKICAgZWxzZQogICAgb3V0cHV0KCcrJykKICAgaiA8LSBqICsgMQogIHVudGlsIChqID4gaSArIDEpCiAgaSA8LSBpICsgMQogdW50aWwgKGkgPiBuICsgMSkKIG91dHB1dCgiRG9uZSIp",
    #     "referencesFileNames": [
    #         "input_1.in",
    #         "input_2.in"
    #     ],
    #     "solutionFileName": "repeat_until.in",
    #     "timeLimit": 10000
    # }
    # print(get_score(SourceGraderRequest(**req)).__dict__)
