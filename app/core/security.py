from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/login',
    refreshUrl='/api/v1/auth/refresh',
    scopes={
        'user:read': 'Read user information',
        'user:create': 'Create user',
        'user:update': 'Update user',
        'user:delete': 'Delete user',
        'nation:create': 'Create nation',
        'nation:read': 'Read nation',
        'nation:update': 'Update nation',
        'nation:delete': 'Delete nation',
        'comment:create': 'Create comment',
        'comment:read': 'Read comment',
        'comment:update': 'Update comment',
        'comment:delete': 'Delete comment',
        'comment:moderate': 'Moderate comments',
        'role:create': 'Create role',
        'role:read': 'Read role',
        'role:update': 'Update role',
        'role:delete': 'Delete role',
        'permission:create': 'Create permission',
        'permission:read': 'Read permission',
        'permission:update': 'Update permission',
        'permission:delete': 'Delete permission',
        'refresh': 'Refresh token access',
    },
)

AccessTokenDep = Annotated[str, Depends(oauth2_scheme)]
