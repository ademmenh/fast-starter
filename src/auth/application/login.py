from src.users.domain.entity import UserEntity
from dataclasses import dataclass
from src.auth.domain.errors import InvalidCredentialsError
from src.auth.domain.ports import IJwtAdapter, IPasswordAdapter, TokenPayload
from src.users.domain.ports import IUserRepository


@dataclass
class TokensOutput:
    access_token: str
    refresh_token: str


@dataclass
class LoginOutput:
    user: UserEntity
    tokens: TokensOutput


@dataclass
class LoginInput:
    email: str
    password: str


class Login:
    def __init__(
        self,
        user_repository: IUserRepository,
        password_adapter: IPasswordAdapter,
        jwt_adapter: IJwtAdapter,
    ) -> None:
        self._user_repository = user_repository
        self._password_adapter = password_adapter
        self._jwt_adapter = jwt_adapter

    async def execute(self, input: LoginInput) -> LoginOutput:
        user = await self._user_repository.find_by_email(input.email)
        if user is None:
            raise InvalidCredentialsError()
        

        is_valid = await self._password_adapter.compare(input.password, user.password_hash)
        if not is_valid:
            raise InvalidCredentialsError()

        payload = TokenPayload(sub=user.id.value, email=user.email.value, role=user.role)

        return LoginOutput(
            user=user,
            tokens=TokensOutput(
                access_token=self._jwt_adapter.sign(payload),
                refresh_token=self._jwt_adapter.sign_refresh(payload),
            ),
        )
