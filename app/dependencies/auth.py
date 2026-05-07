from typing import Annotated, List, Optional

import jwt
from fastapi import Cookie, Depends, HTTPException, Security, status
from fastapi.security import SecurityScopes

from app.core.security import AccessTokenDep
from app.core.settings import settings
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
    except jwt.PyJWTError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        ) from err

    token_scopes = payload.get('scopes', [])

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f'Not enough permissions. Missing scope: {scope}',
                headers={
                    'WWW-Authenticate': f'Bearer scope="{security_scopes.scope_str}"'
                },
            )

    user = await authenticator.authenticate_user(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired token',
        )

    return user


CurrentUserDep = Annotated[User, Security(get_current_user, scopes=[])]


def require_scopes(required_scopes: List[str]):
    async def dependency(
        user: Annotated[User, Security(get_current_user, scopes=required_scopes)],
    ) -> User:
        return user

    return Depends(dependency)
