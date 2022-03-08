import time

from grader.src.ged.classes.edit_path import EditPath
from grader.src.ged.classes.graph import Graph
from grader.src.ged.classes.cost_function import CostFunction
from grader.src.ged.classes.search_node import SearchNode
from grader.src.constants import Constants


class DFSGED:
    """
    precondition:
    - each graph nodes should have component_id in the range [1, len(nodes)]
    - each graph edges should have component_id in the range [len(nodes) + 1, len(nodes) + len(edges)]

    reason for these precondition is to sped up computation
    """
    def __init__(self, source: Graph, target: Graph, cost_function: CostFunction, time_limit=500, sort_node_dfs=False):
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
        self.sort_node_dfs = sort_node_dfs

    def set_use_node_relabel(self, use_node_relabel: bool):
        self.cost_function.clear_precompute()
        self.cost_function.use_node_relabel = use_node_relabel

    def set_time_limit(self, time_limit):
        self.time_limit = time_limit

    def get_node_matching_string(self):
        ret = []
        for k, v in self.ub_path.snode_distortion.items():
            ret.append(f'{k.get_id() : <4} -> {v.get_id()}')
        for k, v in self.ub_path.tnode_distortion.items():
            if v.is_eps():
                ret.append(f'{"EPS" : <4} -> {k.get_id()}')
        return '\n'.join(ret)

    def calculate_edit_distance(self, is_exact_computation=True, approximation_use_node_relabel=None) -> float:
        self.cost_function.clear_precompute()

        # start timer
        self.is_solution_optimal = True
        self.start_time = time.time_ns()

        # process
        snode_size = len(self.source.nodes)
        tnode_size = len(self.target.nodes)
        sedge_size = len(self.source.edges)
        tedge_size = len(self.target.edges)

        ub_cost = Constants.INF

        # creates root
        root = None
        if approximation_use_node_relabel is not None:
            use_node_relabel = self.cost_function.use_node_relabel
            self.set_use_node_relabel(approximation_use_node_relabel)
            root = EditPath.create_root(self.cost_function, self.source, self.target, self.sort_node_dfs)
            self.set_use_node_relabel(use_node_relabel)
        else:
            root = EditPath.create_root(self.cost_function, self.source, self.target, self.sort_node_dfs)

        self.ub_path = EditPath.create_path(self.cost_function, self.source, self.target, root.first_ub)
        self.ub_cost = self.ub_path.predict_cost()

        if is_exact_computation:
            self._search_ged(root)

        return self.ub_cost

    def get_edit_distance(self) -> float:
        return self.ub_cost

    def get_normalized_edit_distance(self) -> float:
        snode_size = len(self.source.nodes)
        tnode_size = len(self.target.nodes)
        sedge_size = len(self.source.edges)
        tedge_size = len(self.target.edges)

        return self.ub_cost / ((snode_size + tnode_size) * self.cost_function.Cost.NODE_COST +
                               (sedge_size + tedge_size) * self.cost_function.Cost.EDGE_COST)

    def _search_ged(self, no_edit: EditPath):
        cur_node = SearchNode(no_edit)

        while cur_node is not None:
            cur_time = time.time_ns()
            if cur_time - self.start_time >= self.time_limit * 1e6:
                self.is_solution_optimal = False
                break

            self._generate_children(cur_node)
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

    def _generate_children(self, search_node: SearchNode):
        edit_path = search_node.edit_path
        if len(edit_path.pending_nodes1):
            node1 = edit_path.pending_nodes1[0]
            for node2 in edit_path.pending_nodes2:
                ch_edit_path = EditPath.clone(edit_path)
                ch_edit_path.add_distortion(node1, node2)
                if ch_edit_path.predict_cost() < self.ub_cost:
                    search_node.add_child(ch_edit_path)

            ch_edit_path = EditPath.clone(edit_path)
            ch_edit_path.add_distortion(node1, Constants.NODE_EPS)
            if ch_edit_path.predict_cost() < self.ub_cost:
                search_node.add_child(ch_edit_path)
