import os
import csv
import subprocess

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
        os.system(f'mkdir -p "{output_folder}"')
        for item in os.listdir(self.tcpath):
            in_path = os.path.join(self.tcpath, item)
            in_name = os.path.splitext(item)[0]
            if (not os.path.isfile(in_path)):
                continue
            out_path = os.path.join(output_folder, f'{in_name}.out')
            
            infile = open(in_path, 'r')
            command = ['python3', self.solution]
            output = subprocess.check_output(command, input=infile.read().encode(), timeout=2)
            infile.close()
            
            outfile = open(out_path, 'w')
            outfile.write(str(output.decode()).rstrip())
            outfile.close()

def get_file_contents(filename):
    file = open(filename, "r")
    file_contents = file.read()
    file.close()
    return file_contents

class Grader:
    def __init__(self):
        pass

    def set_tc_abs(self, path):
        self.tcpath = path
    
    def set_tc_rel(self, path):
        self.tcpath = os.path.join(os.path.dirname(__file__), path)
        
    def set_ans_abs(self, path):
        self.anspath = path
    
    def set_ans_rel(self, path):
        self.anspath = os.path.join(os.path.dirname(__file__), path)

    def grade(self, solution_path):
        correct_count = 0
        output_count = 0

        for item in os.listdir(self.tcpath):
            in_path = os.path.join(self.tcpath, item)
            in_name = os.path.splitext(item)[0]
            out_path = os.path.join(self.anspath, f'{in_name}.out')
            if ((not os.path.isfile(in_path)) or (not os.path.isfile(out_path))):
                continue
            output_count += 1

            infile = open(in_path, 'r')
            command = ['python3', solution_path]
            sol_out = str(subprocess.check_output(command, input=infile.read().encode(), timeout=2).decode()).rstrip()
            infile.close()
            
            reference_out = get_file_contents(out_path).rstrip()

            if (reference_out == sol_out):
                correct_count += 1

        return correct_count / output_count

def generate_outputs(input_path, output_path, solution_file):
    ogenerator = OutputGenerator()
    ogenerator.set_tc_rel(input_path)
    ogenerator.set_solution_rel(solution_file)
    ogenerator.generate_result(output_path)

def grade(input_path, output_path, solution_file):
    grader = Grader()
    grader.set_tc_rel(input_path)
    grader.set_ans_rel(output_path)
    return grader.grade(solution_file)

def generate_and_grade(input_path, output_path, reference_file, solution_file):
    generate_outputs(input_path, output_path, reference_file)
    return grade(input_path, output_path, solution_file)

def grade_all(input_path, output_path, reference_file, solution_path):
    generate_outputs(input_path, output_path, reference_file)
    
    ret = []
    grader = Grader()
    grader.set_tc_rel(input_path)
    grader.set_ans_rel(output_path)
    for item in os.listdir(solution_path):
        py_path = os.path.join(solution_path, item)
        extension = os.path.splitext(item)[1]
        if ((not os.path.isfile(py_path)) or (not extension == ".py")):
            continue
        
        score = grader.grade(py_path)
        ret.append({
            'filename': item,
            'black_box_score': score
        })
        
    return ret

def grade_all_to_csv(input_path, output_path, reference_file, solution_path, csv_file):
    results = grade_all(input_path, output_path, reference_file, solution_path)
    fields = ['filename', 'black_box_score']

    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

if __name__ == '__main__':
    BASE_PATH = '../../datasets/segiempat'
    
    input_path = os.path.join(BASE_PATH, 'in')
    output_path = os.path.join(BASE_PATH, 'out')
    reference_file = os.path.join(BASE_PATH, 'juryssolution/segiempatcontoh.py')
    solution_path = os.path.join(BASE_PATH, 'solution')
    grade_all_to_csv(input_path, output_path, reference_file, solution_path, "test.csv")
        