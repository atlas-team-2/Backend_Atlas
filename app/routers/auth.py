from fastapi import APIRouter, Response

from app.core.responses import auth_responses
from app.dependencies.auth import (
    REFRESH_TOKEN_COOKIE_NAME,
    AuthenticatorDep,
    CurrentUserDep,
    RefreshTokenCookieDep,
    require_scopes,
)
from app.models.entities.user import UserCreate
from app.schemas.auth import (
    AuthData,
    AuthTokenData,
    LogoutResponse,
    MeResponse,
    PasswordResetConfirm,
    RegisterResponse,
)
from app.utils.errors import UnauthorizedError

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/register', response_model=RegisterResponse)
async def register(
    user_create: UserCreate,
    authenticator: AuthenticatorDep,
):
    success = await authenticator.register(user_create)
    return RegisterResponse(success=success)


@router.post('/login', response_model=AuthTokenData, responses=auth_responses)
async def login(
    auth_data: AuthData,
    authenticator: AuthenticatorDep,
    response: Response,
):
    tokens = await authenticator.create_tokens(auth_data)

    if tokens is None:
        raise UnauthorizedError()

    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=tokens.refresh_token,
        httponly=True,
    )

    return tokens


@router.get(
    '/me',
    response_model=MeResponse,
    dependencies=[require_scopes(['user:read'])],
    responses=auth_responses,
)
async def me(current_user: CurrentUserDep):
    return current_user


@router.post('/refresh', response_model=AuthTokenData, responses=auth_responses)
async def refresh(
    authenticator: AuthenticatorDep,
    refresh_token: RefreshTokenCookieDep,
    response: Response,
):
    if refresh_token is None:
        raise UnauthorizedError()

    tokens = await authenticator.refresh_tokens(refresh_token)

    if tokens is None:
        raise UnauthorizedError()

    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=tokens.refresh_token,
        httponly=True,
    )

    return tokens


@router.delete('/logout', response_model=LogoutResponse)
async def logout(
    refresh_token: RefreshTokenCookieDep,
    authenticator: AuthenticatorDep,
    response: Response,
):
    if refresh_token is None:
        return LogoutResponse(success=False)

    success = await authenticator.logout(refresh_token)

    response.delete_cookie(key=REFRESH_TOKEN_COOKIE_NAME)

    return LogoutResponse(success=success)


@router.get('/verify', response_model=RegisterResponse)
async def verify_account(
    email: str,
    code: str,
    authenticator: AuthenticatorDep,
):
    success = await authenticator.verify_account(email, code)
    return RegisterResponse(success=success)


@router.get('/password-reset/send-code', response_model=RegisterResponse)
async def send_password_reset_code(
    email: str,
    authenticator: AuthenticatorDep,
):
    success = await authenticator.send_password_reset_code(email)
    return RegisterResponse(success=success)


@router.post('/password-reset/confirm', response_model=RegisterResponse)
async def confirm_password_reset(
    data: PasswordResetConfirm,
    authenticator: AuthenticatorDep,
):
    success = await authenticator.confirm_password_reset(data.email, data.code, data.new_password)
    return RegisterResponse(success=success)