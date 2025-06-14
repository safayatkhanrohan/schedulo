from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.exceptions.exception import AppException
from app.schema.error import ErrorResponse, ErrorDetail


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """
        Handles all custom application-level exceptions.
        """
        return JSONResponse(status_code=exc.status_code, content=exc.response.dict())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """
        Handles Pydantic validation errors and formats them in a structured error response.
        """
        details = [
            ErrorDetail(
                code=f"validation.{error['type']}",
                message=error["msg"].split(", ", 1)[-1],
                target=".".join(str(loc) for loc in error["loc"] if loc != "body"),
            )
            for error in exc.errors()
        ]

        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                message="Invalid request parameters", details=details
            ).dict(),
        )
