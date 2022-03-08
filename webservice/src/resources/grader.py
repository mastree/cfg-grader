import json

from flask import request
from flask_restful import Resource

from webservice.src.model.grader_response import GraderResponse
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
            req_data = json.loads(data)
            req_data = GraderRequest(**req_data)
            self.logger.info(req_data)
            self.logger.info(type(req_data))

            max_score, min_score, avg_score = get_scores(req_data)
            grader_response = GraderResponse(max_score, min_score, avg_score)
            response = get_response(err=False, msg='Success', data=grader_response)
            self.logger.info("Grading successful!")
            return response
        except Exception as e:
            self.logger.error(f'failed to load json: {e}')
            return get_response(err=True, msg='Failed to parse control flow graph', status_code=500)
