class Portfolio:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_portfolio(self):
        return self.name, self.id
