from dataclasses import dataclass
from src.auth.application.login import TokensOutput
from src.auth.domain.errors import InvalidRefreshTokenError
from src.auth.domain.ports import IJwtAdapter, TokenPayload
from src.users.domain.ports import IUserRepository


@dataclass
class RefreshTokenInput:
    refresh_token: str


class RefreshToken:
    def __init__(
        self,
        user_repository: IUserRepository,
        jwt_adapter: IJwtAdapter,
    ) -> None:
        self._user_repository = user_repository
        self._jwt_adapter = jwt_adapter

    async def execute(self, input: RefreshTokenInput) -> TokensOutput:
        payload = self._jwt_adapter.verify_refresh(input.refresh_token)
        user = await self._user_repository.find_by_id(payload.sub)
        if user is None:
            raise InvalidRefreshTokenError()
        new_payload = TokenPayload(sub=user.id.value, email=user.email.value, role=user.role)
        return TokensOutput(
            access_token=self._jwt_adapter.sign(new_payload),
            refresh_token=self._jwt_adapter.sign_refresh(new_payload),
        )
