from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

OAUTH2_SCOPES = {
    'user:create': 'Create user',
    'user:read': 'Read user information',
    'user:update': 'Update user',
    'user:delete': 'Delete user',
    'nation:create': 'Create nation',
    'nation:read': 'Read nation',
    'nation:update': 'Update nation',
    'nation:delete': 'Delete nation',
    'nation_info:create': 'Create nation info',
    'nation_info:read': 'Read nation info',
    'nation_info:update': 'Update nation info',
    'nation_info:delete': 'Delete nation info',
    'settlement_zone:create': 'Create settlement zone',
    'settlement_zone:read': 'Read settlement zone',
    'settlement_zone:update': 'Update settlement zone',
    'settlement_zone:delete': 'Delete settlement zone',
    'costume:create': 'Create costume',
    'costume:read': 'Read costume',
    'costume:update': 'Update costume',
    'costume:delete': 'Delete costume',
    'game:create': 'Create game',
    'game:read': 'Read game',
    'game:update': 'Update game',
    'game:delete': 'Delete game',
    'game_question:create': 'Create game question',
    'game_question:read': 'Read game question',
    'game_question:update': 'Update game question',
    'game_question:delete': 'Delete game question',
    'game_option:create': 'Create game option',
    'game_option:read': 'Read game option',
    'game_option:update': 'Update game option',
    'game_option:delete': 'Delete game option',
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
}

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/login',
    refreshUrl='/api/v1/auth/refresh',
    scopes=OAUTH2_SCOPES,
)

AccessTokenDep = Annotated[str, Depends(oauth2_scheme)]
