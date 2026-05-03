import asyncio
import bcrypt as _bcrypt
from src.auth.domain.ports import IPasswordAdapter


class PasswordAdapter(IPasswordAdapter):
    async def hash(self, plain: str) -> str:
        salt = _bcrypt.gensalt()
        hashed = await asyncio.to_thread(_bcrypt.hashpw, plain.encode(), salt)
        return hashed.decode()

    async def compare(self, plain: str, hashed: str) -> bool:
        return await asyncio.to_thread(_bcrypt.checkpw, plain.encode(), hashed.encode())
