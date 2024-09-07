from app.errors import messages


class UserNotFoundError(Exception):

    def __init__(self):
        self.message = messages.USER_NOT_FOUND


class UserExistsError(Exception):
    def __init__(self):
        self.message = messages.USER_EXISTS


class InsufficientFundsError(Exception):
    def __init__(self):
        self.message = messages.INSUFFICIENT_FUNDS


class DataBaseError(Exception):
    def __init__(self):
        pass


# class DuplicateKeyError(Exception):
#     def __init__(self):
#         self.message = messages.USER_EXISTS


