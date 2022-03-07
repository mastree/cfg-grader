import time

from grader.src.cfggrader.classes.edit_path import EditPath
from grader.src.cfggrader.classes.graph import Graph
from grader.src.cfggrader.classes.cost_function import CostFunction
from grader.src.cfggrader.classes.search_node import SearchNode
from grader.src.classes.constants import Constants


class DFSGED:
    def __init__(self, source: Graph, target: Graph, cost_function: CostFunction, time_limit: int = 500):
        self.source = source
        self.target = target
        self.cost_function = cost_function
        self.cost_function.set_precompute(source, target)

        # time limit in milliseconds
        self.start_time = None
        self.time_limit = time_limit

        # bound
        self.ub_path: EditPath = None
        self.ub_cost: float = Constants.INF

        self.is_solution_optimal = False

    def set_time_limit(self, time_limit):
        self.time_limit = time_limit

    def print_matching(self):
        for k, v in self.ub_path.snode_distortion.items():
            print(f'{k.component_id : <4} -> {v.component_id}')

    def calculate_edit_distance(self):
        # start timer
        self.is_solution_optimal = True
        self.start_time = time.time_ns()

        # process
        snode_size = len(self.source.nodes)
        tnode_size = len(self.target.nodes)
        sedge_size = len(self.source.edges)
        tedge_size = len(self.target.edges)

        ub_cost = Constants.INF
        root = EditPath.create_root(self.cost_function, self.source, self.target)
        self.ub_path = EditPath.create_path(self.cost_function, self.source, self.target, root.first_ub)
        self.ub_cost = self.ub_path.predict_cost()
        self.search_ged(root)

        return self.ub_cost

    def search_ged(self, no_edit: EditPath):
        cur_node = SearchNode(no_edit)

        while cur_node is not None:
            cur_time = time.time_ns()
            if cur_time - self.start_time >= self.time_limit * 1e6:
                self.is_solution_optimal = False
                break

            self.generate_children(cur_node)
            if len(cur_node.children) == 0:
                edit_path = cur_node.edit_path
                edit_path.complete()
                total_edit_cost = edit_path.predict_cost()
                if self.ub_cost > total_edit_cost:
                    self.ub_cost = total_edit_cost
                    self.ub_path = edit_path
                cur_node = cur_node.parent
                continue

            candidate_node = cur_node.remove_min_child()
            while len(cur_node.children) > 0 and candidate_node.edit_path.predict_cost() > self.ub_cost:
                candidate_node = cur_node.remove_min_child()

            if candidate_node.edit_path.predict_cost() > self.ub_cost:
                candidate_node = cur_node.parent
            cur_node = candidate_node

    def generate_children(self, search_node: SearchNode):
        edit_path = search_node.edit_path
        if len(edit_path.unused_nodes1):
            node1 = edit_path.unused_nodes1[0]
            for node2 in edit_path.unused_nodes2:
                ch_edit_path = EditPath.clone(edit_path)
                ch_edit_path.add_distortion(node1, node2)
                if ch_edit_path.predict_cost() < self.ub_cost:
                    search_node.add_child(ch_edit_path)

            ch_edit_path = EditPath.clone(edit_path)
            ch_edit_path.add_distortion(node1, Constants.NODE_EPS)
            if ch_edit_path.predict_cost() < self.ub_cost:
                search_node.add_child(ch_edit_path)
