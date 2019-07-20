class CardMatch:
    def __init__(self, quantity, name, edition=None):
        self.name = name
        self.quantity = int(quantity)
        self.edition = edition

    def __repr__(self):
        return "<CardMatch : {} [{}] {}>".format(self.quantity, self.edition or '', self.name)

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if int(value) <= 0:
            raise ValueError('Card quantity cannot be zero or negative')
        else:
            self._quantity = value
