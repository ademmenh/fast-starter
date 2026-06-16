from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from src.auth.infrastructure.jwt_adapter import JwtAdapter
from src.auth.infrastructure.password_adapter import PasswordAdapter
from src.auth.module import AuthModule
from src.config.domain.interface import IConfig
from src.config.infrastructure.database_adapter import DatabaseAdapter
from src.controller import AppController
from src.shared.infrastructure.id_generator import IDGenerator
from src.shared.presentation.errors_handlers import (
    generic_error_handler,
    http_exception_handler,
    integrity_error_handler,
    jwt_error_handler,
    validation_error_handler,
)
from src.shared.presentation.open_api import custom_openapi
from src.users.module import UsersModule
from starlette.exceptions import HTTPException as StarletteHTTPException


def create_app(config: IConfig, show_docs: bool = False) -> FastAPI:
    db_adapter = DatabaseAdapter(config)
    jwt_adapter = JwtAdapter(config)
    password_adapter = PasswordAdapter()
    id_generator = IDGenerator()
    engine = db_adapter.engine

    # ── Modules ───────────────────────────────────────────────────────────────────
    auth_module = AuthModule(
        jwt_adapter=jwt_adapter,
        password_adapter=password_adapter,
        id_generator=id_generator,
        engine=engine,
        config=config,
    )
    users_module = UsersModule(
        password_adapter=password_adapter,
        engine=engine,
    )

    router = APIRouter()
    AppController(router)

    # ── Application ───────────────────────────────────────────────────────────────
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        yield

    api_prefix = f"/api/v{config.api_version}"

    app = FastAPI(
        title="Fast Starter API",
        description="FastAPI starter template",
        version=config.api_version,
        lifespan=lifespan,
        docs_url=f"{api_prefix}/docs" if show_docs else None,
        redoc_url=f"{api_prefix}/redoc" if show_docs else None,
        openapi_url=f"{api_prefix}/openapi.json" if show_docs else None,
    )

    app.state.config = config

    # ── Custom OpenAPI ────────────────────────────────────────────────────────────
    def openapi() -> dict:
        schema = get_openapi(
            title="Fast Starter API",
            version=config.api_version,
            description="FastAPI starter template",
            routes=app.routes,
        )
        return custom_openapi(schema)

    app.openapi = openapi

    # ── Exception handlers ────────────────────────────────────────────────────────
    app.exception_handler(StarletteHTTPException)(http_exception_handler)
    app.exception_handler(IntegrityError)(integrity_error_handler)
    app.exception_handler(RequestValidationError)(validation_error_handler)
    app.exception_handler(ValidationError)(validation_error_handler)
    app.exception_handler(JWTError)(jwt_error_handler)
    app.exception_handler(Exception)(generic_error_handler)

    # ── Middleware ─────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=config.cors_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routers ───────────────────────────────────────────────────────────────────
    app.include_router(auth_module.router, prefix=api_prefix)
    app.include_router(users_module.router, prefix=api_prefix)
    app.include_router(router, prefix=api_prefix)

    return app
