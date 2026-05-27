from typing import Annotated, List, Optional

import jwt
from fastapi import Cookie, Depends, Security
from fastapi.security import SecurityScopes

from app.core.security import AccessTokenDep
from app.core.settings import settings
from app.models.entities.user import User
from app.services.authenticator import Authenticator
from app.utils.errors import ForbiddenError, UnauthorizedError

REFRESH_TOKEN_COOKIE_NAME = 'refresh_token'

AuthenticatorDep = Annotated[
    Authenticator,
    Depends(Authenticator),
]

RefreshTokenCookieDep = Annotated[
    Optional[str],
    Cookie(alias=REFRESH_TOKEN_COOKIE_NAME),
]


async def get_current_user(
    security_scopes: SecurityScopes,
    authenticator: AuthenticatorDep,
    token: AccessTokenDep,
) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.auth.secret.get_secret_value(),
            algorithms=[settings.auth.algorithm],
        )
    except jwt.PyJWTError:
        raise UnauthorizedError()

    token_scopes = payload.get('scopes', [])

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise ForbiddenError()

    user = await authenticator.authenticate_user(token)
    if user is None:
        raise UnauthorizedError()

    return user


CurrentUserDep = Annotated[User, Security(get_current_user, scopes=[])]


def require_scopes(required_scopes: List[str]):
    async def dependency(
        user: Annotated[User, Security(get_current_user, scopes=required_scopes)],
    ) -> User:
        return user

    return Depends(dependency)