from fastapi import Depends, HTTPException, Request
from fastapi.security import APIKeyCookie
from src.auth.infrastructure.jwt_adapter import JwtAdapter
from src.auth.domain.ports import TokenPayload

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
    async def __call__(
        self,
        request: Request,
        token: str | None = Depends(access_token_cookie),
    ) -> TokenPayload:
        raw = _extract_token(request, token)
        config = request.app.state.config
        jwt_adapter = JwtAdapter(config)
        return jwt_adapter.verify(raw)


class RefreshTokenGuard:
    async def __call__(
        self,
        request: Request,
        token: str | None = Depends(refresh_token_cookie),
    ) -> TokenPayload:
        raw = _extract_token(request, token)
        config = request.app.state.config
        jwt_adapter = JwtAdapter(config)
        return jwt_adapter.verify_refresh(raw)


class RoleGuard:
    def __init__(self, roles: list[str]):
        self.roles = roles

    async def __call__(
        self,
        request: Request,
        token: str | None = Depends(access_token_cookie),
    ) -> str:
        raw = _extract_token(request, token)
        config = request.app.state.config
        jwt_adapter = JwtAdapter(config)
        payload = jwt_adapter.verify(raw)
        role = getattr(payload, "role", None)
        if role not in self.roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return role
