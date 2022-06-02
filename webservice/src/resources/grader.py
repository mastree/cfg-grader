import json

from flask import request
from flask_restful import Resource

from webservice.src.service.grader import get_scores
from webservice.src.utils.logz import create_logger
from webservice.src.utils.wrapper import get_response
from webservice.src.model.grader_request import *


class Grader(Resource):
    def __init__(self):
        self.logger = create_logger()

    def post(self):
        data = request.data
        self.logger.info("Grading control flow graph...")

        try:
            request_data = json.loads(data)
            request_data = GraderRequest(**request_data)
            self.logger.info(request_data)
            self.logger.info(type(request_data))

            response_data = get_scores(request_data)
            response = get_response(err=False, msg='Success', data=response_data)
            self.logger.info("Grading successful!")
            return response
        except Exception as e:
            self.logger.error(f'An error occurred: {e}')
            return get_response(err=True, msg='Failed to parse control flow graph', status_code=500)
