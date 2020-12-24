from abc import ABC


class Student(ABC):
    def __init__(self, ID, surname, name, patronymic, phone, address, bank_card, debtor, debtor_subjects):
        self.ID = ID
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.phone = phone
        self.address = address
        self.bank_card = bank_card
        self.financial_applications = []

        self.debtor = debtor
        self.debtor_subjects = debtor_subjects

    def get_bank_card(self):
        return self.bank_card

    def get_address(self):
        return self.address

    def get_achievements(self):
        return self.achievements

    def set_financial_applications(self, application):
        self.financial_applications.append(application)

    def set_achievements(self, achievement):
        self.achievements.append(achievement)
