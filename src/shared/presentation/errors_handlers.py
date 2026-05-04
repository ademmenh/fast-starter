from jose import JWTError
from fastapi import Request
from fastapi.responses import JSONResponse
from http import HTTPStatus
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

async def http_exception_handler(_request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": HTTPStatus(exc.status_code).name,
            "statusCode": exc.status_code,
            "message": getattr(exc, "detail", None),
        },
    )

async def jwt_error_handler(_request: Request, exc: JWTError) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={
            "error": HTTPStatus(401).name,
            "statusCode": 401,
            "message": None,
        },
    )

async def integrity_error_handler(_request: Request, exc: IntegrityError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "error": HTTPStatus(409).name,
            "statusCode": 409,
            "message": "Conflict, Duplicate Data.",
        },
    )

async def validation_error_handler(_request: Request, exc: RequestValidationError | ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": HTTPStatus(422).name,
            "statusCode": 422,
            "message": exc.errors(),
        },
    )

async def generic_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error": HTTPStatus(500).name,
            "statusCode": 500,
            "message": None,
        },
    )
