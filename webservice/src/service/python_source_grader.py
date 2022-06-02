from grader.src.cfggenerator.cfggenerator import PythonCfgGenerator
from grader.src.ged.classes.graph import Graph
from grader.src.grader import grade
from webservice.src.model.grader_response_data import GraderResponseData
from webservice.src.model.grading_method import GradingMethod
from webservice.src.model.source_grader_request import SourceGraderRequest


def get_python_scores(grader_request: SourceGraderRequest) -> tuple[int, int, int]:
    solution_source = grader_request.solution
    reference_sources = grader_request.references
    time_limit = grader_request.time_limit
    time_limit_per_unit = grader_request.time_limit_per_unit
    grading_method = grader_request.grading_method

    graph_source = PythonCfgGenerator.generate_python(solution_source)
    graph_targets: list[Graph] = []

    feedback = []
    missing_positions = []
    for reference in reference_sources:
        try:
            graph_targets.append(PythonCfgGenerator.generate_python(reference))
            missing_positions.append(len(feedback))
            feedback.append(-1)
        except Exception as e:
            feedback.append("Failed to generate reference CFG")

    scores, errors, grade_feedback = grade(graph_source, graph_targets, time_limit, time_limit_per_unit)
    for i in range(len(grade_feedback)):
        feedback[missing_positions[i]] = grade_feedback[i]

    score = 0
    if len(scores) > 0:
        if grading_method == GradingMethod.AVERAGE:
            score = sum(scores) / len(scores)
        elif grading_method == GradingMethod.MINIMUM:
            score = min(scores)
        else:
            score = max(scores)

    return GraderResponseData(score, feedback)
