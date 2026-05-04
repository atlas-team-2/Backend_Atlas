from typing import Annotated, Optional

from fastapi import Cookie, Depends, Header, HTTPException, status

from app.models.entities.user import User
from app.services.authenticator import Authenticator

REFRESH_TOKEN_COOKIE_NAME = 'refresh_token'


AuthenticatorDep = Annotated[
    Authenticator,
    Depends(Authenticator),
]

RefreshTokenCookieDep = Annotated[
    Optional[str],
    Cookie(alias=REFRESH_TOKEN_COOKIE_NAME),
]


def _extract_token_from_header(
    authorization: Optional[str],
    token: Optional[str],
) -> Optional[str]:
    if authorization is not None:
        scheme, _, value = authorization.partition(' ')

        if scheme.lower() == 'bearer' and value:
            return value

    return token


async def get_current_user(
    authenticator: AuthenticatorDep,
    authorization: Annotated[Optional[str], Header()] = None,
    token: Annotated[Optional[str], Header()] = None,
) -> User:
    access_token = _extract_token_from_header(authorization, token)

    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access token is required',
        )

    user = await authenticator.authenticate_user(access_token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired access token',
        )

    return user


CurrentUserDep = Annotated[
    User,
    Depends(get_current_user),
]
