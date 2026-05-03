from dataclasses import dataclass
from src.users.domain.errors import UserNotFoundError
from src.users.domain.ports import IUserRepository


@dataclass
class DeleteUserInput:
    user_id: str


class DeleteUser:
    def __init__(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository

    async def execute(self, input: DeleteUserInput) -> None:
        user = await self._user_repository.find_by_id(input.user_id)
        if user is None:
            raise UserNotFoundError(input.user_id)
        await self._user_repository.delete(input.user_id)
