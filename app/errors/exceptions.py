from app.errors.messages import ErrorMessages


class NotFoundError(Exception):

    def __init__(self, ):
        self.message = ErrorMessages.USER_NOT_FOUND


class UserExistsError(Exception):
    def __init__(self):
        self.message = ErrorMessages.USER_EXISTS
