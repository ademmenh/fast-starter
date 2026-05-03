from dataclasses import dataclass
from src.users.domain.entity import UserEntity
from src.users.domain.errors import UserNotFoundError
from src.users.domain.ports import IUserRepository


@dataclass
class GetUserInput:
    user_id: str


class GetUser:
    def __init__(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository

    async def execute(self, input: GetUserInput) -> UserEntity:
        user = await self._user_repository.find_by_id(input.user_id)
        if user is None:
            raise UserNotFoundError(input.user_id)
        return user
