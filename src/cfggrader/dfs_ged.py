import time

from cfggrader.classes.edit_path import EditPath
from cfggrader.classes.graph import Graph
from cfggrader.classes.graph_component import *
from cfggrader.classes.cost_function import CostFunction
from classes.constants import Constants


class DFSGED:
    def __init__(self, source: Graph, target: Graph, cost_function: CostFunction):
        self.source = source
        self.target = target
        self.cost_function = cost_function
        self.cost_function.set_precompute(source, target)

        # time limit in milliseconds
        self.time_limit = 500

    def set_time_limit(self, time_limit):
        self.time_limit = time_limit

    def calculate_edit_distance(self):
        # start timer
        start_time = time.time_ns()

        # process
        snode_size = len(self.source.nodes)
        tnode_size = len(self.target.nodes)
        sedge_size = len(self.source.edges)
        tedge_size = len(self.target.edges)

        ub_cost = Constants.INF
        root = EditPath.create_root(self.cost_function, self.source, self.target)
        ub_path = EditPath.create_path(self.cost_function, self.source, self.target, root.first_ub)

        # end timer
        end_time = time.time_ns()

        return ub_path.total_cost
