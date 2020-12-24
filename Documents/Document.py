from abc import ABC


class Document(ABC):
    def __init__(self, ID, name, date, filled=False, confirmed=False, published=False):
        self.ID = ID
        self.name = name
        self.date = date
        self.filled = filled
        self.confirmed = confirmed
        self.published = published

    def set_filled(self, filled):
        self.filled = filled

    def set_confirmed(self, confirmed):
        self.confirmed = confirmed

    def set_published(self, published):
        self.published = published
