from fastapi import APIRouter, HTTPException, Response, status

from app.dependencies.auth import (
    REFRESH_TOKEN_COOKIE_NAME,
    AuthenticatorDep,
    CurrentUserDep,
    RefreshTokenCookieDep,
)
from app.models.entities.user import UserCreate
from app.schemas.auth import (
    AuthData,
    AuthTokenData,
    LogoutResponse,
    MeResponse,
    RegisterResponse,
)


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


@router.post('/login', response_model=AuthTokenData)
async def login(
    auth_data: AuthData,
    authenticator: AuthenticatorDep,
    response: Response,
):
    tokens = await authenticator.create_tokens(auth_data)

    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password',
        )

    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=tokens.refresh_token,
        httponly=True,
    )

    return tokens


@router.get('/me', response_model=MeResponse)
async def me(
    current_user: CurrentUserDep,
):
    return current_user


@router.post('/refresh', response_model=AuthTokenData)
async def refresh(
    refresh_token: RefreshTokenCookieDep,
    authenticator: AuthenticatorDep,
    response: Response,
):
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token is required',
        )

    tokens = await authenticator.refresh_tokens(refresh_token)

    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired refresh token',
        )

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

    response.delete_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
    )

    return LogoutResponse(success=success)
