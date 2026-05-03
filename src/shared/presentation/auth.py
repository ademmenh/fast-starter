from dataclasses import dataclass
from fastapi import Depends, HTTPException, Request
from fastapi.security import APIKeyCookie
from src.auth.infrastructure.jwt_adapter import JwtAdapter


@dataclass
class AuthUser:
    id: str
    email: str
    role: str


access_token_cookie = APIKeyCookie(name="access_token", auto_error=False)
refresh_token_cookie = APIKeyCookie(name="refresh_token", auto_error=False)


def _extract_token(request: Request, cookie_token: str | None) -> str:
    if cookie_token:
        return cookie_token
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1]
    raise HTTPException(status_code=401, detail="Missing authentication token")


class AccessTokenGuard:
    """Verifies access tokens. Use on all protected endpoints."""

    async def __call__(
        self,
        request: Request,
        token: str | None = Depends(access_token_cookie),
    ) -> AuthUser:
        raw = _extract_token(request, token)
        config = request.app.state.config
        jwt_adapter = JwtAdapter(config)

        payload = jwt_adapter.verify(raw)
        if payload is None:
            raise HTTPException(status_code=401, detail="Missing authentication token")

        return AuthUser(id=payload.sub, email=payload.email, role=payload.role)


class RefreshTokenGuard:
    """Verifies refresh tokens. Use only on /auth/refresh."""

    async def __call__(
        self,
        request: Request,
        token: str | None = Depends(refresh_token_cookie),
    ) -> str:
        raw = _extract_token(request, token)
        config = request.app.state.config
        jwt_adapter = JwtAdapter(config)

        payload = jwt_adapter.verify_refresh(raw)
        if payload is None:
            raise HTTPException(status_code=401, detail="Missing authentication token")

        return raw


class RoleGuard:
    def __init__(self, roles: list[str]):
        self.roles = roles

    async def __call__(self, current_user: AuthUser = Depends(AccessTokenGuard())) -> AuthUser:
        if current_user.role not in self.roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user

