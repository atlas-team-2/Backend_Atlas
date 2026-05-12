from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError


class Hasher:
    password_hash = PasswordHash.recommended()

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.password_hash.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        try:
            return cls.password_hash.verify(plain_password, hashed_password)
        except UnknownHashError:
            return False
