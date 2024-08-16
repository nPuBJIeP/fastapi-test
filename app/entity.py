class User:
    id: int
    balance: float  # todo change to decimal(why?)

    def __init__(self, user_id: int, balance: float):
        self.id = user_id
        self.balance = balance

