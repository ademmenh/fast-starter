from src.users.domain.entity import UserRole
from fastapi import Depends, Query
from src.shared.presentation.auth import AccessTokenGuard, RoleGuard, TokenPayload
from src.shared.presentation.responses import (
    PaginatedResponse,
    PaginationMeta,
    Response,
)
from src.users.application.delete_user import DeleteUser, DeleteUserInput
from src.users.application.get_user import GetUser, GetUserInput
from src.users.application.list_users import ListUsers, ListUsersInput
from src.users.application.update_user import UpdateUser, UpdateUserInput
from src.users.domain.errors import UserEmailAlreadyExistsError, UserNotFoundError
from src.users.presentation.dtos import UpdateUserDto
from src.users.presentation.exception_handler import UsersExceptionHandler
from src.users.presentation.rdtos import UserRDTO
from typing import Annotated

class UsersController:
    def __init__(
        self,
        router,
        exception_handler: UsersExceptionHandler,
        list_users_use_case: ListUsers,
        get_user_use_case: GetUser,
        update_user_use_case: UpdateUser,
        delete_user_use_case: DeleteUser,
    ) -> None:
        self.router = router
        self.exception_handler = exception_handler
        self.list_users_use_case = list_users_use_case
        self.get_user_use_case = get_user_use_case
        self.update_user_use_case = update_user_use_case
        self.delete_user_use_case = delete_user_use_case
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.get("/users", response_model=PaginatedResponse[UserRDTO])(self.list_users)
        self.router.get(
            "/users/{user_id}",
            response_model=Response[UserRDTO],
            responses={"404": {"description": "USER_NOT_FOUND: User with id not found"}},
        )(self.get_user)
        self.router.put(
            "/users/{user_id}",
            response_model=Response[UserRDTO],
            responses={
                "404": {"description": "USER_NOT_FOUND: User with id not found"},
                "409": {"description": "USER_EMAIL_ALREADY_EXISTS: User with email already exists"},
            },
        )(self.update_user)
        self.router.delete(
            "/users/{user_id}",
            status_code=204,
            responses={"404": {"description": "USER_NOT_FOUND: User with id not found"}},
        )(self.delete_user)

    async def list_users(
        self,
        _current_user: Annotated[TokenPayload, Depends(AccessTokenGuard())],
        _role_user: Annotated[TokenPayload, Depends(RoleGuard(["admin"]))],
        page: Annotated[int, Query(ge=1, description="Page number")] = 1,
        limit: Annotated[int, Query(ge=1, le=32, description="Items per page")] = 20,
        role: UserRole | None = Query(None, description="Filter by role"),
        search: str | None = Query(None, description="Search by name or email"),
    ) -> PaginatedResponse[UserRDTO]:
        try:
            users, total = await self.list_users_use_case.execute(
                ListUsersInput(role=role, search=search, page=page, limit=limit)
            )
            return PaginatedResponse(
                message="Users retrieved successfully",
                status_code=200,
                data=[UserRDTO.from_entity(u) for u in users],
                pagination=PaginationMeta(total=total, page=page, limit=limit),
            )
        except Exception as exc:
            self.exception_handler(exc)

    async def get_user(
        self,
        user_id: str,
        _current_user: Annotated[TokenPayload, Depends(AccessTokenGuard())],
        _role: Annotated[TokenPayload, Depends(RoleGuard(["admin"]))]
    ) -> Response[UserRDTO]:
        try:
            user = await self.get_user_use_case.execute(GetUserInput(user_id=user_id))
            return Response(
                message="User retrieved successfully",
                status_code=200,
                data=UserRDTO.from_entity(user),
            )
        except UserNotFoundError as exc:
            self.exception_handler(exc)

    async def update_user(
        self,
        user_id: str,
        dto: UpdateUserDto,
        _current_user: Annotated[TokenPayload, Depends(AccessTokenGuard())],
        _role: Annotated[TokenPayload, Depends(RoleGuard(["admin"]))]
    ) -> Response[UserRDTO]:
        try:
            user = await self.update_user_use_case.execute(
                UpdateUserInput(
                    user_id=user_id,
                    name=dto.name,
                    email=dto.email,
                    phone=dto.phone,
                    password=dto.password,
                    role=dto.role,
                )
            )
            return Response(
                message="User updated successfully",
                status_code=200,
                data=UserRDTO.from_entity(user),
            )
        except (UserNotFoundError, UserEmailAlreadyExistsError) as exc:
            self.exception_handler(exc)

    async def delete_user(
        self,
        user_id: str,
        _current_user: Annotated[TokenPayload, Depends(AccessTokenGuard())],
        _role: Annotated[TokenPayload, Depends(RoleGuard(["admin"]))]
    ) -> None:
        try:
            await self.delete_user_use_case.execute(DeleteUserInput(user_id=user_id))
        except UserNotFoundError as exc:
            self.exception_handler(exc)
