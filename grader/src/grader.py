import math

from grader.src.api.functions import edit_distance_to_similarity_score
from grader.src.constants import Constants
from grader.src.ged.classes.cost_function import CostFunction
from grader.src.ged.classes.general_cost_function import GeneralCostFunction
from grader.src.ged.classes.graph import Graph
from grader.src.ged.dfs_ged import DFSGED
from grader.src.ged.utils.graph_collapser import *


class GraphPreprocess:
    UNCOLLAPSE = 0
    COLLAPSE = 1
    COLLAPSE_AND_PROPAGATE_BRANCHING = 2


def preprocess_graph(graph: Graph, preproc):
    if preproc == GraphPreprocess.UNCOLLAPSE:
        graph = uncollapse(graph)
    elif preproc == GraphPreprocess.COLLAPSE:
        graph = collapse(graph)
    elif preproc == GraphPreprocess.COLLAPSE_AND_PROPAGATE_BRANCHING:
        graph = propagate_branching(graph)
    return graph


def grade_one_on_one(graph_source: Graph,
                     graph_target: Graph,
                     cost_function: CostFunction=None,
                     node_key: str = "label") -> float:
    if cost_function is None:
        cost_function = GeneralCostFunction(node_key=node_key)

    dfs_ged = DFSGED(graph_source, graph_target, cost_function)
    dfs_ged.calculate_edit_distance()
    score = edit_distance_to_similarity_score(dfs_ged.get_normalized_edit_distance())

    return score * Constants.MAX_SCORE


def grade(graph_source: Graph,
          graph_targets: list[Graph],
          use_node_relabel=True,
          graph_preprocess=GraphPreprocess.COLLAPSE_AND_PROPAGATE_BRANCHING,
          node_key: str = "label") -> tuple[list, list]:
    graph_source = preprocess_graph(graph_source, graph_preprocess)
    cost_function = GeneralCostFunction(use_node_relabel=use_node_relabel, node_key=node_key)
    scores = []
    errors = []

    for rgraph_target in graph_targets:
        graph_target = preprocess_graph(rgraph_target, graph_preprocess)
        try:
            score = grade_one_on_one(graph_source, graph_target, cost_function)
            scores.append(score)
        except Exception as e:
            errors.append(e)

    return scores, errors
