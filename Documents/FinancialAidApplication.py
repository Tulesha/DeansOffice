from enum import Enum
from Documents.Document import Document


class Cause(Enum):
    financial_position = 1
    disability = 2
    lostParent = 3


class FinancialAidApplication(Document):
    def __init__(self, ID, name, date, student_surname, cause):
        super().__init__(ID, name, date)
        self.student_ID = student_surname
        self.cause = cause

    def get_cause(self):
        return self.cause
