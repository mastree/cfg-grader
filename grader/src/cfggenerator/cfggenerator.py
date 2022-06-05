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
            current = {
                "rawLine": (astor.to_source(statement)).split('\n')[0],
                "label": cls._get_statement_type_string(statement)
            }
            info.append(current)
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
        id_node = {}
        for block in cfg:
            node = cls._block_to_node(block)
            id_node[node.get_id()] = node
            last_id = max(last_id, node.get_id())
            graph.add_node(node)

        for block in cfg:
            for out_edge in block.exits:
                from_node = id_node[out_edge.source.id]  # graph.find_node_with_id(out_edge.source.id)
                to_node = id_node[out_edge.target.id]  # graph.find_node_with_id(out_edge.target.id)

                last_id += 1
                edge = Edge(last_id, from_node, to_node)

                from_node.add_edge(edge)
                if from_node.get_id() != to_node.get_id():
                    to_node.add_edge(edge)

                graph.add_edge(edge)

        # Add an exit for 'if' blocks with only one exit
        new_nodes = []
        for node in graph.nodes:
            if len(node.info) > 0 and node.info[-1]['label'].lower() == 'if' and len(node.out_edges) == 1:
                last_id += 1
                new_node = Node(last_id)
                last_id += 1
                new_edge = Edge(last_id, node, new_node)

                node.add_edge(new_edge)
                new_node.add_edge(new_edge)
                new_nodes.append(new_node)
                graph.add_edge(new_edge)

        for new_node in new_nodes:
            graph.add_node(new_node)

        return graph

    @classmethod
    def draw_python_from_file(cls, filename, img_filename):
        cfg = CFGBuilder().build_from_file("", filename)
        cfg = cls._compress_blocks_id(cfg)
        cfg.build_visual(img_filename, "jpg")

    @classmethod
    def generate_python(cls, raw_code) -> Graph:
        cfg = CFGBuilder().build_from_src("", raw_code)
        return cls._cfg_to_graph(cfg)

    @classmethod
    def generate_python_from_file(cls, filename) -> Graph:
        with open(filename, 'r') as file:
            raw_code = file.read()
            return cls.generate_python(raw_code)
