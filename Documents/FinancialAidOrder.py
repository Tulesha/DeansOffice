from Documents.Document import Document


class FinancialAidOrder(Document):
    def __init__(self, ID, name, date):
        super().__init__(ID, name, date)
        self.students = []
        self.amounts = []

    def set_student_amount(self, student, amount):
        self.students.append(student)
        self.amounts.append(amount)

    def get_students_amounts(self):
        return self.students, self.amounts
