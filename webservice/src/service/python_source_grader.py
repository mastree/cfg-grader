from grader.src.cfggenerator.cfggenerator import PythonCfgGenerator
from grader.src.ged.classes.graph import Graph
from grader.src.grader import grade


def get_python_scores(solution_source, jury_solution_sources) -> tuple[float, float, float]:
    graph_source = PythonCfgGenerator.generate_pyton(solution_source)
    graph_targets: list[Graph] = []

    for jury_solution in jury_solution_sources:
        try:
            graph_targets.append(PythonCfgGenerator.generate_pyton(jury_solution))
        except Exception as e:
            continue

    scores = grade(graph_source, graph_targets)
    max_score = max(scores)
    min_score = min(scores)
    avg_score = sum(scores) / len(scores)

    return max_score, min_score, avg_score