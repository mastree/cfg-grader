from flask import Flask
from flask_restful import Api

from webservice.src.resources.health_check import HealthCheck
from webservice.src.resources.grader import Grader
from webservice.src.resources.python_source_grader import PythonSourceGrader

app = Flask(__name__)
api = Api(app)

api.add_resource(HealthCheck, '/healthcheck')
api.add_resource(PythonSourceGrader, '/grade-source')
api.add_resource(Grader, '/grade')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
