class User:
    id: int
    balance: float  # todo change to decimal(why?)

    def __init__(self, user_id: int, balance: float):
        self.id = user_id
        self.balance = balance


class BalanceAdd:
    user_id: int
    amount: float

    def __init__(self, user_id: int, amount: float):
        self.user_id = user_id
        self.amount = amount


class BalanceWithdraw:
    user_id: int
    amount: float

    def __init__(self, user_id: int, amount: float):
        self.user_id = user_id
        self.amount = amount


class BalanceTransfer:
    sender_id: int
    recipient_id: int
    amount: float

    def __init__(self, sender_id: int, recipient_id: int, amount: float):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.amount = amount


class UserToUserTransfer:
    sender: User
    recipient: User

    def __init__(self, sender: User, recipient: User):
        self.sender = sender
        self.recipient = recipient
