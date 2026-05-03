from .application.login import Login
from .application.refresh import RefreshToken
from .application.register import Register
from .presentation.controllers import AuthController
from .presentation.exception_handler import AuthExceptionHandler
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncEngine
from src.auth.infrastructure.jwt_adapter import JwtAdapter
from src.auth.infrastructure.password_adapter import PasswordAdapter
from src.shared.infrastructure.id_generator import IDGenerator
from src.users.infrastructure.repository import UserRepository
from src.config.domain.interface import IConfig


class AuthModule:
    def __init__(
        self,
        jwt_adapter: JwtAdapter,
        password_adapter: PasswordAdapter,
        id_generator: IDGenerator,
        engine: AsyncEngine,
        config: IConfig,
    ) -> None:
        router = APIRouter()
        user_repo = UserRepository(engine)

        register_use_case = Register(
            user_repository=user_repo,
            password_adapter=password_adapter,
            id_generator=id_generator,
            jwt_adapter=jwt_adapter,
        )
        login_use_case = Login(user_repo, password_adapter, jwt_adapter)
        refresh_use_case = RefreshToken(user_repo, jwt_adapter)

        exception_handler = AuthExceptionHandler()
        AuthController(
            router=router,
            register_use_case=register_use_case,
            login_use_case=login_use_case,
            refresh_use_case=refresh_use_case,
            exception_handler=exception_handler,
            config=config,
        )
        self.router: APIRouter = router
