class InvalidCredentialsError(Exception):
    code = "INVALID_CREDENTIALS"

    def __init__(self) -> None:
        super().__init__("Invalid email or password")


class InvalidRefreshTokenError(Exception):
    code = "INVALID_REFRESH_TOKEN"

    def __init__(self) -> None:
        super().__init__("Invalid or expired refresh token")
