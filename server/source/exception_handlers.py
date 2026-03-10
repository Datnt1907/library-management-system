from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from source.exceptions import DefaultError


async def library_exception_handler(
    request: Request, exc: DefaultError
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "error_code": exc.error_code,
            "message": exc.message,
        },
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Custom handler for FastAPI/Pydantic validation errors.
    Transforms the default validation error format to match DefaultError structure.
    """
    errors = []

    for error in exc.errors():
        errors.append(
            {
                "type": error.get("type", ""),
                "location": list(error.get("loc", [])),
                "message": error.get("msg", ""),
                "input": error.get("input"),
            }
        )
    return JSONResponse(
        status_code=422,
        content={
            "status_code": 422,
            "error_code": "VALIDATION_ERROR",
            "message": "Validation Error",
            "detail": errors,
        },
    )


def add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        RequestValidationError,
        request_validation_exception_handler,  # type: ignore
    )

    app.add_exception_handler(DefaultError, library_exception_handler)  # type: ignore
