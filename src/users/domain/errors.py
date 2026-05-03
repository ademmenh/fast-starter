class UserNotFoundError(Exception):
    code = "USER_NOT_FOUND"

    def __init__(self, user_id: str) -> None:
        super().__init__(f'User with id "{user_id}" not found')


class UserEmailAlreadyExistsError(Exception):
    code = "USER_EMAIL_ALREADY_EXISTS"

    def __init__(self, email: str) -> None:
        super().__init__(f'User with email "{email}" already exists')


class UnauthorizedUserOperationError(Exception):
    code = "UNAUTHORIZED_USER_OPERATION"

    def __init__(self) -> None:
        super().__init__("You do not have permission to perform this action")
