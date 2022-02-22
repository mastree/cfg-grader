import math
from cfggrader.classes.graph_component import *


class Constants:
    INF = math.inf
    MAX_SCORE = 100

    EDGE_EPS = Edge()
    NODE_EPS = Node()

    node_cost_matrix: list[list] = None
    edge_cost_matrix: list[list] = None

