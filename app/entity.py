class User:
    id: int
    balance: float  # todo change to decimal(why?)

    def __init__(self, user_id: int, balance: float):
        self.id = user_id
        self.balance = balance


class BalanceAdd:
    user_id: int
    amount: float


class BalanceWithdraw:
    user_id: int
    amount: float


class BalanceTransfer:
    from_user_id: int
    to_user_id: int
    amount: float
