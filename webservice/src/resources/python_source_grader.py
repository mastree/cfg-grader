import json

from flask import request
from flask_restful import Resource

from webservice.src.model.source_grader_request import SourceGraderRequest
from webservice.src.service.python_source_grader import get_python_scores
from webservice.src.utils.logz import create_logger
from webservice.src.utils.wrapper import get_response


class PythonSourceGrader(Resource):
    def __init__(self):
        self.logger = create_logger()

    def post(self):
        data = request.data
        self.logger.info("Grading python source...")

        try:
            request_data = json.loads(data)
            request_data = SourceGraderRequest(**request_data)
            self.logger.info(request_data)
            self.logger.info(type(request_data))

            response_data = get_python_scores(request_data)
            response = get_response(err=False, msg='Success', data=response_data)
            self.logger.info("Grading successful!")
            return response
        except Exception as e:
            self.logger.error(f'An error occurred: {e}')
            return get_response(err=True, msg=f'An error occurred: {e.__class__.__name__}', status_code=500)
