class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class InvalidCredentialsException(AppException):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, status_code=401)

class UserAlreadyExistsException(AppException):
    def __init__(self, message: str = "User already exists"):
        super().__init__(message, status_code=409)