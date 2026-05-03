from src.shared.presentation.responses import CamelModel


class AuthUserRDTO(CamelModel):
    id: str = "<uuid>"
    name: str = "John Doe"
    email: str = "johnDoe@gmail.com"
    role: str = "admin"


class AuthTokensRDTO(CamelModel):
    access_token: str
    refresh_token: str
