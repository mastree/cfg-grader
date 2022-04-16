from flask import request
from flask_restful import Resource

from webservice.src.model.grader_response import GraderResponse
from webservice.src.service.python_source_grader import get_python_scores
from webservice.src.utils.check_file import check_file
from webservice.src.utils.logz import create_logger
from webservice.src.utils.wrapper import get_response


class PythonSourceGrader(Resource):
    def __init__(self):
        self.logger = create_logger()

    def post(self):
        if 'src_refs' not in request.files:
            return get_response(err=True,
                                msg='Reference sources are required, please include "src_refs" files!', status_code=400)
        if 'src' not in request.files:
            return get_response(err=True, msg='Source is required, please include "src" file!', status_code=400)

        jury_solution_sources = request.files.getlist("src_refs")
        solution_source = request.files["src"]

        files = jury_solution_sources + [solution_source]
        for file in files:
            err_file, msg_file = check_file(file)
            if err_file:
                return get_response(err=err_file, msg=msg_file, status_code=400)

        jury_solution_sources = [src.read().decode("UTF-8") for src in jury_solution_sources]
        solution_source = solution_source.read().decode("UTF-8")
        try:
            self.logger.info("Grading python source...")

            max_score, min_score, avg_score = get_python_scores(solution_source, jury_solution_sources)
            grader_response = GraderResponse(max_score, min_score, avg_score)
            response = get_response(err=False, msg='Success', data=grader_response)
            self.logger.info("Grading successful!")
            return response
        except Exception as e:
            self.logger.error(f'An error occurred: {e}')
            return get_response(err=True, msg=f'An error occurred: {e.__class__.__name__}', status_code=500)
