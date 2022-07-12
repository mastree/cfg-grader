import base64

from webservice.src.model.grading_method import GradingMethod


class SourceGraderRequest:
    def __init__(self, solution,
                 solutionFileName,
                 references,
                 referencesFileNames,
                 timeLimit=5000,
                 timeLimitPerUnit=3000,
                 gradingMethod=GradingMethod.MAXIMUM.name,
                 language="Python",
                 **kwargs):
        self.solution = base64.b64decode(solution).decode('utf-8')
        self.solution_file_name = solutionFileName
        self.references: list[str] = []
        self.references_file_names = referencesFileNames
        self.time_limit = timeLimit
        self.time_limit_per_unit = max(self.time_limit // max(len(self.references), 1), timeLimitPerUnit)
        self.grading_method = GradingMethod[gradingMethod.upper()]
        self.language = language

        for reference in references:
            self.references.append(base64.b64decode(reference).decode('utf-8'))
