from flask_restful import Resource

from webservice.src.utils.logz import create_logger
from webservice.src.utils.wrapper import get_response


class HealthCheck(Resource):
    def __init__(self):
        self.logger = create_logger()

    def get(self):
        self.logger.info("receiving health check endpoint")
        return get_response(err=False, msg='Healthy')
