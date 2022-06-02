import json
from http import HTTPStatus

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
        request_data = None

        try:
            request_data = json.loads(data)
            request_data = GraderRequest(**request_data)
        except Exception as e:
            self.logger.error(f'Bad request: {e}')
            return get_response(
                err=True, msg='invalid request body', status_code=HTTPStatus.BAD_REQUEST)

        try:
            response_data = get_scores(request_data)
            self.logger.info("Grading successful!")
            return get_response(err=False, msg='success', data=response_data, status_code=HTTPStatus.OK)
        except Exception as e:
            self.logger.error(f'An error occurred: {e}')
            return get_response(
                err=True, msg='an error occured', status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
