from http import HTTPStatus

from flask_restful import Resource

from web_service.src.utils.logz import create_logger
from web_service.src.utils.wrapper import get_response


class Description(Resource):
    def __init__(self):
        self.logger = create_logger()

    def get(self):
        self.logger.info("Description requested.")
        responseData = {
            "imageName": "kamalshafi/cfg-similarity-grader",
            "displayedName": "White Box Structural Autograder",
            "description": "Structural White Box Autograder Using Control Flow Graph Similarity (currently for Python only)",
        }
        return get_response(err=False, msg="success", data=responseData, status_code=HTTPStatus.ACCEPTED)
