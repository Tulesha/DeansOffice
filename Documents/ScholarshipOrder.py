from Documents.Document import Document


class ScholarshipOrder(Document):
    def __init__(self, ID, name, date):
        super().__init__(ID, name, date)
        self.budgets = []
        self.scholarships = []

    def set_budget_scholarship(self, budget, scholarship):
        self.budgets.append(budget)
        self.scholarships.append(scholarship)

    def get_budgets_scholarships(self):
        return self.budgets, self.scholarships
