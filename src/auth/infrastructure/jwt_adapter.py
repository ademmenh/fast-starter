from datetime import UTC, datetime, timedelta
from jose import jwt
from src.auth.domain.ports import IJwtAdapter, TokenPayload
from src.config.domain.interface import IConfig

class JwtAdapter(IJwtAdapter):
    def __init__(self, config: IConfig) -> None:
        self._config = config

    def sign(self, payload: TokenPayload) -> str:
        expire = datetime.now(UTC) + timedelta(seconds=self._config.jwt_access_token_expiry)
        data = {
            "sub": payload.sub,
            "email": payload.email,
            "role": payload.role,
            "exp": expire,
        }
        return jwt.encode(data, self._config.jwt_access_token_secret, algorithm=self._config.jwt_algo)

    def verify(self, token: str) -> TokenPayload:
        data = jwt.decode(
            token, 
            self._config.jwt_access_token_secret, 
            algorithms=[self._config.jwt_algo]
        )
        return TokenPayload(sub=data["sub"], email=data["email"], role=data["role"])

    def sign_refresh(self, payload: TokenPayload) -> str:
        expire = datetime.now(UTC) + timedelta(seconds=self._config.jwt_refresh_token_expiry)
        data = {
            "sub": payload.sub,
            "email": payload.email,
            "role": payload.role,
            "exp": expire,
        }
        return jwt.encode(data, self._config.jwt_refresh_token_secret, algorithm=self._config.jwt_algo)

    def verify_refresh(self, token: str) -> TokenPayload | None:
        data = jwt.decode(
            token, 
            self._config.jwt_refresh_token_secret, 
            algorithms=[self._config.jwt_algo]
        )
        return TokenPayload(sub=data["sub"], email=data["email"], role=data["role"])
