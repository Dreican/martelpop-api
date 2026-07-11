import asyncio
from dataclasses import dataclass
from typing import NamedTuple

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

@dataclass(frozen=True, slots=True)
class PasswordVerificationResult:
    valid: bool
    updated_hash: str | None


class PasswordService:
    def __init__(self) -> None:
        self._password_hash = PasswordHash(
            (Argon2Hasher(),)
        )

    async def hash_password(self, password: str) -> str:
        return await asyncio.to_thread(self._password_hash.hash, password)


    def verify_password(self, password: str, password_hash: str) -> bool:
        return self._password_hash.verify(password, password_hash)

    def verify_and_update(self, password: str, password_hash: str) -> PasswordVerificationResult:
        valid, updated_hash = self._password_hash.verify_and_update(password, password_hash)
        return PasswordVerificationResult(
            valid=valid,
            updated_hash=updated_hash,
        )
