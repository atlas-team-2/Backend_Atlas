from pwdlib import PasswordHash


class Hasher:
    password_hash = PasswordHash.recommended()

    @staticmethod
    def get_password_hash(password: str) -> str:
        return Hasher.password_hash.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return Hasher.password_hash.verify(plain_password, hashed_password)
