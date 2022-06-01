from pycfg.pycfg import PyCFG, CFGNode, slurp

class CfgGenerator:
    @classmethod
    def generate_pyton(cls, raw_code):
        CFGNode.cache = {}
        cfg = PyCFG()
        cfg.gen_cfg(raw_code.strip())
        return CFGNode.to_Graph([])

    @classmethod
    def generate_python_from_file(cls, filename):
        CFGNode.cache = {}
        cfg = PyCFG() 
        cfg.gen_cfg(slurp(filename).strip())
        g = CFGNode.to_graph([])
        return g
