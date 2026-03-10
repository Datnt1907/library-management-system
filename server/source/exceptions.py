from typing import Any, ClassVar, Literal

from pydantic import BaseModel, Field, create_model


class DefaultError(Exception):
    """
    Base exception class for all errors raised by Library Management.

    A custom exception handler for FastAPI takes care
    of catching and returning a proper HTTP error from them.

    Args:
        message: The error message that'll be displayed to the user.
        status_code: The status code of the HTTP response. Defaults to 500.
        error_code: Machine-readable error code.
    """

    _schema: ClassVar[type[BaseModel] | None] = None

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_SERVER_ERROR",
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

    @classmethod
    def schema(cls) -> type[BaseModel]:
        if cls._schema is not None:
            return cls._schema

        error_literal = Literal[cls.__name__]  # type: ignore

        model = create_model(
            cls.__name__,
            error=(error_literal, Field(examples=[cls.__name__])),
            detail=(str, ...),
            error_code=(str, ...),
        )
        cls._schema = model
        return cls._schema


class BadRequest(DefaultError):
    def __init__(
        self,
        message: str = "Bad request",
        status_code: int = 400,
        error_code: str = "BAD_REQUEST",
    ) -> None:
        super().__init__(message, status_code, error_code)


class NotPermitted(DefaultError):
    def __init__(
        self,
        message: str = "Not permitted",
        status_code: int = 403,
        error_code: str = "NOT_PERMITTED",
    ) -> None:
        super().__init__(message, status_code, error_code)


class Unauthorized(DefaultError):
    def __init__(
        self,
        message: str = "Unauthorized",
        status_code: int = 401,
        error_code: str = "UNAUTHORIZED",
    ) -> None:
        super().__init__(message, status_code, error_code)


class InternalServerError(DefaultError):
    def __init__(
        self,
        message: str = "Internal Server Error",
        status_code: int = 500,
        error_code: str = "INTERNAL_SERVER_ERROR",
    ) -> None:
        super().__init__(message, status_code, error_code)


class ResourceNotFound(DefaultError):
    def __init__(
        self,
        message: str = "Not found",
        status_code: int = 404,
        error_code: str = "RESOURCE_NOT_FOUND",
    ) -> None:
        super().__init__(message, status_code, error_code)


class ResourceUnavailable(DefaultError):
    def __init__(
        self,
        message: str = "Unavailable",
        status_code: int = 410,
        error_code: str = "RESOURCE_UNAVAILABLE",
    ) -> None:
        super().__init__(message, status_code, error_code)


class ResourceAlreadyExists(DefaultError):
    def __init__(
        self,
        message: str = "Already exists",
        status_code: int = 409,
        error_code: str = "RESOURCE_ALREADY_EXISTS",
    ) -> None:
        super().__init__(message, status_code, error_code)


# Custom Validation Error
class ValidationErrorDetail(BaseModel):
    type: str
    location: list[str | int]
    message: str
    input: Any | None = None


class ValidationErrorResponse(BaseModel):
    status_code: int
    error_code: str
    message: str
    detail: list[ValidationErrorDetail]
