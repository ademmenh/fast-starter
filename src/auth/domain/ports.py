from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TokenPayload:
    sub: str
    email: str
    role: str


class IJwtAdapter(ABC):
    @abstractmethod
    def sign(self, payload: TokenPayload) -> str: ...

    @abstractmethod
    def verify(self, token: str) -> TokenPayload | None: ...

    @abstractmethod
    def sign_refresh(self, payload: TokenPayload) -> str: ...

    @abstractmethod
    def verify_refresh(self, token: str) -> TokenPayload | None: ...


class IPasswordAdapter(ABC):
    @abstractmethod
    async def hash(self, plain: str) -> str: ...

    @abstractmethod
    async def compare(self, plain: str, hashed: str) -> bool: ...
