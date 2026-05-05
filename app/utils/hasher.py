import hashlib
import hmac
import os


class Hasher:
    @staticmethod
    def get_password_hash(password: str, salt: bytes | None = None) -> str:
        if salt is None:
            salt = os.urandom(16)
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
        return salt.hex() + ':' + hashed.hex()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        try:
            salt_hex, hash_hex = hashed_password.split(':')
            salt = bytes.fromhex(salt_hex)
            expected_hash = bytes.fromhex(hash_hex)
            test_hash = hashlib.pbkdf2_hmac(
                'sha256', plain_password.encode(), salt, 100_000
            )
            return hmac.compare_digest(test_hash, expected_hash)
        except Exception:
            return False
