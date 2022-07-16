from flask import Flask
from flask_restful import Api

from web_service.src.resources.health_check import HealthCheck
from web_service.src.resources.grader import Grader
from web_service.src.resources.source_grader import SourceGrader

from web_service.src.resources.description import Description

app = Flask(__name__)
api = Api(app)

api.add_resource(HealthCheck, '/health-check')
api.add_resource(Description, '/description')
api.add_resource(SourceGrader, '/grade')
api.add_resource(Grader, '/grade-cfg')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
