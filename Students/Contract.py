from Students.Student import Student


class Contract(Student):
    def __init__(self, ID, surname, name, patronymic, phone, address, bank_card, debtor, debtor_subjects, receipts, fix):
        super().__init__(ID, surname, name, patronymic, phone, address, bank_card, debtor, debtor_subjects)
        self.receipts = receipts
        self.fix = fix

    def get_receipts(self):
        return self.receipts

    def add_receipts(self, receipt):
        self.receipts.append(receipt)

    def set_fix(self, fix):
        self.fix = fix
