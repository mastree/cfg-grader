import json

from http import HTTPStatus
from flask import request
from flask_restful import Resource

from web_service.src.model.source_grader_request import SourceGraderRequest
from web_service.src.service.source_grader import get_score
from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import get_response


class SourceGrader(Resource):
    def __init__(self):
        self.logger = create_logger()

    def post(self):
        data = request.data
        self.logger.info("Grading python source...")
        request_data = None

        try:
            request_data = json.loads(data)
            request_data = SourceGraderRequest(**request_data)
        except Exception as e:
            self.logger.error(f'Bad request: {e}')
            return get_response(
                err=True, msg='invalid request body', status_code=HTTPStatus.BAD_REQUEST)

        try:
            response_data = get_score(request_data)
            self.logger.info("Grading successful!")
            return get_response(err=False, msg='success', data=response_data, status_code=HTTPStatus.OK)
        except Exception as e:
            self.logger.error(f'An error occurred: {e}')
            return get_response(
                err=True, msg=f'an error occured: {e.__class__.__name__}', status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
