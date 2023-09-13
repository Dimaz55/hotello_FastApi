from fastapi import HTTPException


class NotFoundException(HTTPException):
    status_code = 404
    detail = "entity not found"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class RoomNotFoundException(NotFoundException):
    detail = "room not found"


class HotelNotFoundException(NotFoundException):
    detail = "hotel not found"


class BookingNotFoundException(NotFoundException):
    detail = "booking not found"


class ConflictException(HTTPException):
    status_code = 409

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

    
class UserExistsException(ConflictException):
    detail = "user already exists"


class RoomIsBusyException(ConflictException):
    detail = "room is busy for your dates"


class UnauthenticatedException(HTTPException):
    status_code = 401
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectCredentialsException(UnauthenticatedException):
    detail = "incorrect credentials"


class TokenExpiredException(UnauthenticatedException):
    detail = "token expired"


class NoTokenException(UnauthenticatedException):
    detail = "No token"


class WrongTokenException(UnauthenticatedException):
    detail = "Wrong token format"


class ValidationError(HTTPException):
    detail = "Validation error"
    status_code = 400

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class DatesValidationError(ValidationError):
    def __init__(self, detail=None):
        self.detail = detail
        super().__init__()
