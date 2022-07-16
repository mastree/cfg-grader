import base64

from web_service.src.model.grading_method import GradingMethod
from web_service.src.utils.check_file import get_extension


def get_file_language(filename):
    ext = get_extension(filename)
    if ext in ['py', 'ipynb']:
        return 'python'
    else:
        return 'notal'


class SourceGraderRequest:
    def __init__(self, solution,
                 solutionFileName,
                 references,
                 referencesFileNames,
                 timeLimit=5000,
                 timeLimitPerUnit=3000,
                 gradingMethod=GradingMethod.MAXIMUM.name,
                 language=None,
                 **kwargs):
        self.solution = base64.b64decode(solution).decode('utf-8')
        self.solution_file_name = solutionFileName
        self.references = [base64.b64decode(reference).decode('utf-8') for reference in references]
        self.references_file_names = referencesFileNames
        self.time_limit = timeLimit
        self.time_limit_per_unit = max(self.time_limit // max(len(self.references), 1), timeLimitPerUnit)
        self.grading_method = GradingMethod[gradingMethod.upper()]
        self.language = language
        if language is None:
            self.language = get_file_language(self.solution_file_name)
