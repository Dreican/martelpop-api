from typing import NamedTuple

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher


class PasswordVerificationResult(NamedTuple):
    valid: bool
    updated_hash: str | None


class PasswordService:
    def __init__(self) -> None:
        self._ph = PasswordHash(
            (Argon2Hasher(),)
        )

    def hash_password(self, password: str) -> str:
        return self._ph.hash(password)


    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self._ph.verify(password, hashed_password)

    def verify_and_update(self, password: str, hashed_password: str) -> PasswordVerificationResult:
        valid, updated_hash = self._ph.verify_and_update(password, hashed_password)
        return PasswordVerificationResult(
            valid=valid,
            updated_hash=updated_hash,
        )
