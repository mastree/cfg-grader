import math

from grader.src.api.functions import edit_distance_to_similarity_score
from grader.src.classes.graph import Graph
from grader.src.constants import Constants
from grader.src.ged.classes.cost_function import CostFunction
from grader.src.ged.classes.general_cost_function import GeneralCostFunction
from grader.src.ged.dfs_ged import DFSGED
from grader.src.ged.utils.graph_collapser import collapse, uncollapse


def grade_one_on_one(graph_source: Graph, graph_target: Graph, cost_function: CostFunction=None) -> float:
    if cost_function is None:
        cost_function = GeneralCostFunction()

    dfs_ged = DFSGED(graph_source, graph_target, cost_function)
    dfs_ged.calculate_edit_distance()
    score = edit_distance_to_similarity_score(dfs_ged.get_normalized_edit_distance(), math.sqrt)

    return score * Constants.MAX_SCORE


def grade(graph_source: Graph, graph_targets: list[Graph], collapse_graph: bool = True):
    if collapse_graph:
        graph_source = collapse(graph_source)
    else:
        graph_source = uncollapse(graph_source)

    cost_function = GeneralCostFunction()
    scores = []

    for rgraph_target in graph_targets:
        graph_target = rgraph_target
        if collapse_graph:
            graph_target = collapse(rgraph_target)
        else:
            graph_target = uncollapse(rgraph_target)
        scores.append(grade_one_on_one(graph_source, graph_target, cost_function))

    return scores
