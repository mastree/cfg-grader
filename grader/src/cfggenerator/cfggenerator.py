import astor
from staticfg import CFGBuilder, CFG, Block

from grader.src.ged.classes.graph import Graph
from grader.src.ged.classes.graph_component import Node, Edge


class PythonCfgGenerator:
    @classmethod
    def _get_statement_type_string(cls, statement):
        ret = type(statement).__name__.lower()
        if ret == "for" or ret == "while":
            ret = "for/while"
        return ret

    @classmethod
    def _block_to_node(cls, block: Block):
        info = []
        for statement in block.statements:
            info.append({
                "rawLine": (astor.to_source(statement)).split('\n')[0],
                "label": cls._get_statement_type_string(statement)
            })
        node = Node(block.id, info)
        return node

    @classmethod
    def _compress_blocks_id(cls, cfg: CFG, start=1):
        for block in cfg:
            block.id = start
            start += 1
        return cfg

    @classmethod
    def _cfg_to_graph(cls, cfg: CFG):
        cls._compress_blocks_id(cfg)

        graph = Graph()
        last_id = 0
        for block in cfg:
            node = cls._block_to_node(block)
            last_id = max(last_id, node.component_id)
            graph.add_node(node)

        for block in cfg:
            for out_edge in block.exits:
                from_node = graph.find_node_with_id(out_edge.source.id)
                to_node = graph.find_node_with_id(out_edge.target.id)

                last_id += 1
                edge = Edge()
                edge.set_id(last_id)
                edge.set_from_node(from_node)
                edge.set_to_node(to_node)

                from_node.add_edge(edge)
                to_node.add_edge(edge)

                graph.add_edge(edge)

        return graph

    @classmethod
    def draw_python_from_file(cls, filename, img_filename):
        cfg = CFGBuilder().build_from_file("", filename)
        cfg = cls._compress_blocks_id(cfg)
        cfg.build_visual(img_filename, "jpg")

    @classmethod
    def generate_pyton(cls, raw_code) -> Graph:
        cfg = CFGBuilder().build_from_src("", raw_code)
        return cls._cfg_to_graph(cfg)

    @classmethod
    def generate_python_from_file(cls, filename) -> Graph:
        cfg = CFGBuilder().build_from_file("", filename)
        return cls._cfg_to_graph(cfg)
