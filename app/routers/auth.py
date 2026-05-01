from fastapi import APIRouter, HTTPException, Response, status

from app.core.settings import settings
from app.dependencies.auth import (
    REFRESH_TOKEN_COOKIE_NAME,
    AuthenticatorDep,
    CurrentUserDep,
    RefreshTokenCookieDep,
)
from app.models.entities.user import UserCreate, UserPublic
from app.schemas.auth import AuthData, AuthTokenData, LogoutResponse

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


def _set_refresh_token_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        samesite='lax',
        max_age=int(settings.auth.refresh_token_lifetime.total_seconds()),
    )


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    authenticator: AuthenticatorDep,
    response: Response,
) -> AuthTokenData:
    tokens = await authenticator.register(user_create)

    _set_refresh_token_cookie(response, tokens.refresh_token)
    return tokens


@router.post('/login')
async def login(
    auth_data: AuthData,
    authenticator: AuthenticatorDep,
    response: Response,
) -> AuthTokenData:
    tokens = await authenticator.create_tokens(auth_data)

    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    _set_refresh_token_cookie(response, tokens.refresh_token)
    return tokens


@router.get('/me')
async def me(current_user: CurrentUserDep) -> UserPublic:
    return current_user


@router.post('/logout')
async def logout(
    authenticator: AuthenticatorDep,
    refresh_token: RefreshTokenCookieDep,
    response: Response,
) -> LogoutResponse:
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token cookie is required',
        )

    success = await authenticator.logout(refresh_token)

    if success:
        response.delete_cookie(key=REFRESH_TOKEN_COOKIE_NAME)

    return LogoutResponse(success=success)


@router.post('/refresh')
async def refresh(
    authenticator: AuthenticatorDep,
    refresh_token: RefreshTokenCookieDep,
    response: Response,
) -> AuthTokenData:
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token cookie is required',
        )

    tokens = await authenticator.refresh_tokens(refresh_token)

    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired refresh token',
        )

    _set_refresh_token_cookie(response, tokens.refresh_token)
    return tokens
