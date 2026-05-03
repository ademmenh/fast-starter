from dataclasses import dataclass
from src.auth.application.login import LoginOutput, TokensOutput
from src.auth.domain.ports import IJwtAdapter, IPasswordAdapter, TokenPayload
from src.shared.domain.email import Email
from src.shared.domain.phone import Phone
from src.shared.infrastructure.id_generator import IDGenerator
from src.users.domain.entity import UserEntity
from src.users.domain.errors import UserEmailAlreadyExistsError
from src.users.domain.ports import IUserRepository


@dataclass
class RegisterInput:
    name: str
    email: str
    password: str
    phone: str | None = None


class Register:
    def __init__(
        self,
        user_repository: IUserRepository,
        password_adapter: IPasswordAdapter,
        id_generator: IDGenerator,
        jwt_adapter: IJwtAdapter,
    ) -> None:
        self._user_repository = user_repository
        self._password_adapter = password_adapter
        self._id_generator = id_generator
        self._jwt_adapter = jwt_adapter

    async def execute(self, input: RegisterInput) -> LoginOutput:
        existing_user = await self._user_repository.find_by_email(input.email)
        if existing_user:
            raise UserEmailAlreadyExistsError(input.email)

        user = UserEntity(
            id=self._id_generator.generate(),
            name=input.name,
            email=Email.create(input.email),
            phone=Phone.create(input.phone) if input.phone else None,
            password_hash=await self._password_adapter.hash(input.password),
            role="client",
        )

        saved_user = await self._user_repository.create(user)

        payload = TokenPayload(
            sub=saved_user.id.value,
            email=saved_user.email.value,
            role=saved_user.role,
        )

        return LoginOutput(
            user=saved_user,
            tokens=TokensOutput(
                access_token=self._jwt_adapter.sign(payload),
                refresh_token=self._jwt_adapter.sign_refresh(payload),
            ),
        )
