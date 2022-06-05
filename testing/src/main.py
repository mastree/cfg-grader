import csv
import os.path

import pandas as pd
from definitions import ROOT_DIR
from grader.src.cfggenerator.cfggenerator import PythonCfgGenerator
from grader.src.grader import grade


def read_results_data(filename):
    file_path = os.path.join(ROOT_DIR, "datasets", "results", filename)
    ret = pd.read_excel(file_path, index_col=0)
    return ret


def generate_source_cfgs(dirname, filename):
    dir_path = os.path.join(ROOT_DIR, "datasets", dirname)
    folders = [f for f in os.listdir(dir_path)]
    for folder in folders:
        source_root = os.path.join(dir_path, folder)
        if filename in os.listdir(source_root):
            source_path = os.path.join(dir_path, folder, filename)
            nim = folder.split()[0]
            cur_cfg = None
            try:
                cur_cfg = PythonCfgGenerator.generate_python_from_file(source_path)
            except Exception as e:
                cur_cfg = None
                # print(e)
            yield nim, cur_cfg


def generate_reference_cfgs(dirname):
    dir_path = os.path.join(ROOT_DIR, "datasets", "references", dirname)
    ret = []
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        ret.append(PythonCfgGenerator.generate_python_from_file(file_path))
    return ret


def write_csv(filename, columns, data=list[dict]):
    csv_path = os.path.join(ROOT_DIR, "datasets", "csv", filename)
    with open(csv_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)


if __name__ == '__main__':
    praktikum3_dirs = [
        "4658 Praktikum 3 Shift 1 - 07.30-09.30",
        "4659 Praktikum 3 Shift 2 - 10.00-12.00",
        "4660 Praktikum 3 Shift 3 - 13.00-15.00",
        "4661 Praktikum 3 Shift 4 - 15.45-17.45"
    ]
    praktikum6_dirs = [
        "4918 Praktikum 6 - Shift 1 (08.00 - 10.00)",
        "4919 Praktikum 6 - Shift 2 (10.00 - 12.00)",
        "4920 Praktikum 6 - Shift 3 (13.00 - 15.00)",
        "4921 Praktikum 6 - Shift 4 (15.45 - 17.45)"
    ]
    data = read_results_data("segiempat.xlsx")
    # print(data.iloc[:10])
    # print(data.columns.tolist())
    unit_time_limit = 3000
    references = generate_reference_cfgs("segiempat")
    students_score = {}
    for nim, cfg in generate_source_cfgs(praktikum3_dirs[-1], "segiempat.py"):
        print(f"Grading student {nim}...")
        if cfg is None:
            students_score[nim] = 0
            continue
        scores, _, _ = grade(cfg, references, unit_time_limit * (len(references) + 1), unit_time_limit)
        students_score[nim] = max(scores)

    new_data = []
    for nim, kamal_score in students_score.items():
        row = data.loc[int(nim)]
        blackbox_score = row["Blackscore"]
        kevin_score = row["Whitescore"]
        new_data.append({
            'nim': int(nim),
            'bb_score': blackbox_score,
            'old_wb_score': kevin_score,
            'new_wb_score': kamal_score
        })
    csv_columns = ['nim', 'bb_score', 'old_wb_score', 'new_wb_score']
    write_csv("segitiga.csv", csv_columns, new_data)
