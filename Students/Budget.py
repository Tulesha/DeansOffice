from Students.Student import Student


class Budget(Student):
    def __init__(self, ID, surname, name, patronymic, phone, address, bank_card, debtor, debtor_subjects, scholarship):
        super().__init__(ID, surname, name, patronymic, phone, address, bank_card, debtor, debtor_subjects)
        self.scholarship = scholarship

    def set_scholarship(self, scholarship):
        self.scholarship = scholarship

    def get_scholarship(self):
        return self.scholarship
