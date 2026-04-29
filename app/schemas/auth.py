from pydantic import BaseModel, SecretStr

from app.models.entities.user import UserPublic


class AuthData(BaseModel):
    email: str
    password: SecretStr


class AuthTokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class RegisterResponse(BaseModel):
    success: bool


class LogoutResponse(BaseModel):
    success: bool


class MeResponse(UserPublic):
    pass
