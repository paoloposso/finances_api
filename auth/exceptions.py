class UserAlreadyExistsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidDataException(Exception):
    def __init__(self, message):
        super().__init__(message)
