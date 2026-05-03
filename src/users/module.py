from .application.delete_user import DeleteUser
from .application.get_user import GetUser
from .application.list_users import ListUsers
from .application.delete_user import DeleteUser
from .application.update_user import UpdateUser
from .infrastructure.repository import UserRepository
from .presentation.controllers import UsersController
from .presentation.exception_handler import UsersExceptionHandler
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncEngine
from src.auth.infrastructure.password_adapter import PasswordAdapter

class UsersModule:
    def __init__(
        self,
        password_adapter: PasswordAdapter,
        engine: AsyncEngine,
    ) -> None:
        router = APIRouter()
        user_repo = UserRepository(engine)

        list_users_use_case = ListUsers(user_repo)
        get_user_use_case = GetUser(user_repo)
        update_user_use_case = UpdateUser(user_repo, password_adapter)
        delete_user_use_case = DeleteUser(user_repo)

        exception_handler = UsersExceptionHandler()
        controller = UsersController(
            router,
            exception_handler,
            list_users_use_case,
            get_user_use_case,
            update_user_use_case,
            delete_user_use_case,
        )
        self.router: APIRouter = controller.router
