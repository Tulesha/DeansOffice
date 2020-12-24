class BankCard:
    def __init__(self, number, shel_life, amount):
        self.number = number
        self.shel_life = shel_life
        self.amount = amount

    def add_amount(self, amount):
        self.amount += amount
