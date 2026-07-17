"""Global exception handlers."""

import logging

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.common.responses import ErrorDetail, make_error_response

logger = logging.getLogger(__name__)


def _request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "unknown")


async def request_validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Return validation errors in the standard response envelope."""
    errors = [
        ErrorDetail(
            field=".".join(str(loc) for loc in err["loc"] if loc != "body"),
            message=str(err["msg"]),
        )
        for err in exc.errors()
    ]
    response = make_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        dev_code="VALIDATION_ERROR",
        message="Request validation failed",
        request_id=_request_id(request),
        errors=errors,
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(response),
    )


async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Return unexpected errors in the standard response envelope."""
    logger.error("Unexpected error: %s", exc, exc_info=True)
    response = make_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        dev_code="INTERNAL_ERROR",
        message="An unexpected error occurred",
        request_id=_request_id(request),
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(response),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register application exception handlers."""
    # Starlette's add_exception_handler types handlers as Exception-wide; FastAPI
    # still dispatches the concrete exception type at runtime.
    app.add_exception_handler(RequestValidationError, request_validation_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unexpected_error_handler)
