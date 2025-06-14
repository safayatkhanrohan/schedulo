from fastapi import status
from fastapi.exceptions import HTTPException
from app.schema.error import ErrorResponse, ErrorDetail


class AppException(HTTPException):
    def __init__(
        self,
        message: str,
        code: str,
        target: str = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        self.status_code = status_code
        self.response = ErrorResponse(
            message=message,
            details=[ErrorDetail(code=code, message=message, target=target)],
        )
        super().__init__(status_code=status_code, detail=message)


class InvalidCredentialsException(AppException):
    def __init__(self):
        super().__init__(
            message="Invalid email or password",
            code="auth.invalid_credentials",
            target="email_or_password",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class UserAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(
            message="User already exists with this email",
            code="user.already_exists",
            target="email",
            status_code=status.HTTP_409_CONFLICT,
        )
class UnAuthenticatedException(AppException):
    def __init__(self):
        super().__init__(
            message="You are not authenticated",
            code="auth.unauthenticated",
            target="authentication",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class InvalidTokenException(AppException):
    def __init__(self):
        super().__init__(
            message="Invalid or expired token",
            code="auth.invalid_token",
            target="token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class TimeSlotConflictException(AppException):
    def __init__(self):
        super().__init__(
            message="This time slot overlaps with an existing available slot.",
            code="timeslot.conflict",
            target="time_slot",
            status_code=status.HTTP_409_CONFLICT,
        )
