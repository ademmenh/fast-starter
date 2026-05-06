from src.shared.presentation.responses import ApiResponse
from src.auth.presentation.rdtos import AuthTokensRDTO
from fastapi import APIRouter, Depends, Response as FastAPIResponse
from src.auth.application.login import Login, LoginInput
from src.auth.application.refresh import RefreshToken, RefreshTokenInput
from src.auth.domain.errors import InvalidCredentialsError, InvalidRefreshTokenError
from src.auth.presentation.dtos import LoginDto, RegisterDto
from src.auth.presentation.exception_handler import AuthExceptionHandler
from src.auth.presentation.rdtos import AuthUserRDTO
from src.shared.presentation.auth import RefreshTokenGuard
from src.shared.presentation.responses import AuthApiResponse, TokensData
from src.users.domain.errors import UserEmailAlreadyExistsError
from src.auth.application.register import Register, RegisterInput
from src.config.domain.interface import IConfig

class AuthController:
    def __init__(
        self,
        router: APIRouter,
        exception_handler: AuthExceptionHandler,
        register_use_case: Register,
        login_use_case: Login,
        refresh_use_case: RefreshToken,
        config: IConfig,
    ) -> None:
        self.router = router
        self.exception_handler = exception_handler
        self.register_use_case = register_use_case
        self.login_use_case = login_use_case
        self.refresh_use_case = refresh_use_case
        self._config = config
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.post(
            "/auth/login",
            response_model=AuthApiResponse[AuthUserRDTO],
            responses={"401": {"description": "INVALID_CREDENTIALS: Invalid email or password"}},
        )(self.login)
        self.router.post(
            "/auth/register",
            response_model=AuthApiResponse[AuthUserRDTO],
            status_code=201,
            responses={"409": {"description": "USER_EMAIL_ALREADY_EXISTS: User with email already exists"}},
        )(self.register)
        self.router.post(
            "/auth/refresh",
            response_model=ApiResponse[AuthTokensRDTO],
        )(self.refresh)

    def _set_auth_cookies(self, response: FastAPIResponse, access_token: str, refresh_token: str) -> None:
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite=self._config.cookies_same_site,  # type: ignore[arg-type]
            secure=self._config.cookies_secure,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite=self._config.cookies_same_site,  # type: ignore[arg-type]
            secure=self._config.cookies_secure,
        )

    async def login(
        self,
        dto: LoginDto,
        response: FastAPIResponse,
    ) -> AuthApiResponse[AuthUserRDTO]:
        try:
            result = await self.login_use_case.execute(LoginInput(email=dto.email, password=dto.password))
            self._set_auth_cookies(response, result.tokens.access_token, result.tokens.refresh_token)
            return AuthApiResponse(
                message="Login successful",
                status_code=200,
                data=AuthUserRDTO(
                    id=result.user.id.value,
                    name=result.user.name,
                    email=result.user.email.value,
                    role=result.user.role,
                ),
                tokens=TokensData(
                    access_token=result.tokens.access_token,
                    refresh_token=result.tokens.refresh_token,
                ),
            )
        except InvalidCredentialsError as exc:
            self.exception_handler(exc)

    async def register(
        self,
        dto: RegisterDto,
        response: FastAPIResponse,
    ) -> AuthApiResponse[AuthUserRDTO]:
        try:
            result = await self.register_use_case.execute(
                RegisterInput(
                    name=dto.name,
                    email=dto.email,
                    password=dto.password,
                    phone=dto.phone,
                )
            )
            self._set_auth_cookies(response, result.tokens.access_token, result.tokens.refresh_token)
            return AuthApiResponse(
                message="Registration successful",
                status_code=201,
                data=AuthUserRDTO(
                    id=result.user.id.value,
                    name=result.user.name,
                    email=result.user.email.value,
                    role=result.user.role
                ),
                tokens=TokensData(
                    access_token=result.tokens.access_token,
                    refresh_token=result.tokens.refresh_token,
                ),
            )
        except UserEmailAlreadyExistsError as exc:
            self.exception_handler(exc)

    async def refresh(
        self,
        response: FastAPIResponse,
        refresh_token: str = Depends(RefreshTokenGuard()),
    ) -> ApiResponse[AuthTokensRDTO]:
        try:
            result = await self.refresh_use_case.execute(RefreshTokenInput(refresh_token=refresh_token))
            self._set_auth_cookies(response, result.access_token, result.refresh_token)
            return ApiResponse(
                message="Token refreshed",
                status_code=200,
                data=AuthTokensRDTO(
                    access_token=result.access_token,
                    refresh_token=result.refresh_token,
                ),
            )
        except InvalidRefreshTokenError as exc:
            self.exception_handler(exc)
