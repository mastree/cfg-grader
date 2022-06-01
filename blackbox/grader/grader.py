import os

class OutputGenerator:
    def __init__(self):
        pass
        
    def set_tc_abs(self, path):
        self.tcpath = path
    
    def set_tc_rel(self, path):
        self.tcpath = os.path.join(os.path.dirname(__file__), path)
    
    def set_solution_abs(self, path):
        self.solution = path
    
    def set_solution_rel(self, path):
        self.solution = os.path.join(os.path.dirname(__file__), path)
    
    def generate_result(self, output_folder):
        result = []
        os.system(f'mkdir -p {output_folder}')
        for item in os.listdir(self.tcpath):
            itemabs = os.path.join(self.tcpath, item)
            itemname = os.path.splitext(item)[0]
            if (not os.path.isfile(itemabs)):
                continue
            os.system(f'cat {itemabs} | python3 {self.solution} >> {output_folder}/{itemname}.out')
            # print(item)

if __name__ == '__main__':
    BASE_PATH = '../../datasets/segiempat'
    
    ogenerator = OutputGenerator()
    ogenerator.set_tc_rel(os.path.join(BASE_PATH, 'in'))
    ogenerator.set_solution_rel(os.path.join(BASE_PATH, 'solution/segiempatcontoh.py'))
    
    ogenerator.generate_result(os.path.join(BASE_PATH, 'out'))
        