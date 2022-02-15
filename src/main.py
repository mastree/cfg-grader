# from pycfg_ex import generate_cfg
from cfggenerator.cfggenerator import *
from api.functions import *

cfg = PythonCfgGenerator.generate_python_from_file("../datasets/segiempat/juryssolution/segiempatcontoh.py")
# print(cfg)

print(type(cfg))
digraph_to_graph(cfg)
