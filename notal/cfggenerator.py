from grader.src.ged.classes.graph import Graph
from notal.cfg_generator.src.api.functions import get_cfg
from notal.intermediate.src.classes.graph import Graph as IGraph
from notal.intermediate.src.utils.utils import graph_to_grader_graph


class NotalCfgGenerator:
    def generate_from_source(self, source) -> Graph:
        igraph = IGraph(get_cfg(None, src=source, use_expression_type=True))
        graph = graph_to_grader_graph(igraph)
        return graph
