from cfggenerator.python.cfggenerator import PythonCfgGenerator
from api.functions import *

from cfggrader.utils.graph_collapser import *


cfg = PythonCfgGenerator.generate_python_from_file("../datasets/segiempat/juryssolution/segiempatcontoh.py")
# print(cfg)

graph = digraph_to_graph(cfg)
cgraph = collapse(graph)

digraph = graph_to_digraph(graph)
digraph.draw('generatedimg/digraph2.png', prog='dot')


cdigraph = graph_to_digraph(cgraph)
cdigraph.draw('generatedimg/digraph_collapsed2.png', prog='dot')

# print(digraph)
# print("====================================")
# print(cdigraph)