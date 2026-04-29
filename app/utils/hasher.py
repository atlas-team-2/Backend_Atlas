import base64
import hashlib
import hmac
import secrets

try:
    from pwdlib import PasswordHash
except ImportError:  # pragma: no cover
    PasswordHash = None


class Hasher:
    _password_hash = PasswordHash.recommended() if PasswordHash is not None else None
    _iterations = 600_000

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        if Hasher._password_hash is not None:
            return Hasher._password_hash.verify(plain_password, hashed_password)

        try:
            _, iterations, salt, expected_hash = hashed_password.split('$')
        except ValueError:
            return False

        actual_hash = Hasher.__pbkdf2_hash(
            plain_password,
            salt,
            int(iterations),
        )
        return hmac.compare_digest(actual_hash, expected_hash)

    @staticmethod
    def get_password_hash(password: str) -> str:
        if Hasher._password_hash is not None:
            return Hasher._password_hash.hash(password)

        salt = secrets.token_hex(16)
        password_hash = Hasher.__pbkdf2_hash(
            password,
            salt,
            Hasher._iterations,
        )
        return f'pbkdf2_sha256${Hasher._iterations}${salt}${password_hash}'

    @staticmethod
    def __pbkdf2_hash(password: str, salt: str, iterations: int) -> str:
        digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            iterations,
        )
        return base64.urlsafe_b64encode(digest).decode()
