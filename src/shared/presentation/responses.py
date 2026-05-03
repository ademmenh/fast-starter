from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class PaginationMeta(CamelModel):
    total: int
    page: int
    limit: int


class TokensData(CamelModel):
    access_token: str
    refresh_token: str


class Response[T](CamelModel):
    message: str
    status_code: int = 200
    data: T


class PaginatedResponse[T](CamelModel):
    message: str = "Successful response"
    status_code: int = 200
    data: list[T]
    pagination: PaginationMeta


class AuthApiResponse[T](CamelModel):
    message: str = "Successful response"
    status_code: int = 200
    data: T
    tokens: TokensData

class ApiResponse[T](CamelModel):
    message: str = "Successful response"
    status_code: int = 200
    data: T
