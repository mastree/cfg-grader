# from pycfg_ex import generate_cfg
from cfggenerator.cfggenerator import *

cfg = CfgGenerator.generate_python_from_file("../datasets/segiempat/solution/segiempatcontoh.py")
print(cfg)
print(type(cfg))
