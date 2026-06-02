from sqlalchemy import delete
from sqlmodel import select

from app.core.rbac import PERMISSIONS_MAP
from app.core.security import OAUTH2_SCOPES
from app.core.settings import settings
from app.models.entities.link_models import RolePermission, UserRole
from app.models.entities.permission import Permission
from app.models.entities.role import Role
from app.models.entities.user import User
from app.repositories.permission import PermissionRepository
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.utils.hasher import Hasher


class Bootstrapper:
    def __init__(
        self,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
        user_repository: UserRepository,
    ):
        self._role_repo = role_repository
        self._perm_repo = permission_repository
        self._user_repo = user_repository

    async def _get_or_create_permission(self, subject: str, action: str) -> Permission:
        permission = await self._perm_repo.get_by_scope(subject, action)

        if permission is None:
            permission = Permission(subject=subject, action=action)
            self._role_repo.session.add(permission)
            await self._role_repo.session.flush()

        return permission

    async def _get_or_create_role(self, name: str, description: str) -> Role:
        role = await self._role_repo.get_by_name(name)

        if role is None:
            role = Role(name=name, description=description)
            self._role_repo.session.add(role)
            await self._role_repo.session.flush()

        return role

    async def _replace_role_permissions(
        self,
        role: Role,
        permissions: list[Permission],
    ) -> None:
        await self._role_repo.session.execute(
            delete(RolePermission).where(RolePermission.role_id == role.id),
        )

        self._role_repo.session.add_all(
            [
                RolePermission(role_id=role.id, permission_id=permission.id)
                for permission in permissions
            ],
        )

    async def _ensure_user_has_role(self, user: User, role: Role) -> None:
        statement = select(UserRole).where(
            UserRole.user_id == user.id,
            UserRole.role_id == role.id,
        )
        result = await self._role_repo.session.execute(statement)

        if result.scalar_one_or_none() is None:
            self._role_repo.session.add(
                UserRole(user_id=user.id, role_id=role.id),
            )

    async def bootstrap(self) -> None:
        all_permissions: list[Permission] = []

        for scope in OAUTH2_SCOPES:
            if scope == 'refresh':
                continue

            subject, action = scope.split(':', 1)
            permission = await self._get_or_create_permission(subject, action)
            all_permissions.append(permission)

        admin_role = await self._get_or_create_role(
            name=settings.rbac.admin_role,
            description='Administrator with full access',
        )
        await self._replace_role_permissions(
            role=admin_role,
            permissions=all_permissions,
        )

        for role_name, scopes in PERMISSIONS_MAP.items():
            role = await self._get_or_create_role(
                name=role_name,
                description=f'{role_name.capitalize()} role',
            )

            role_permissions = [
                permission
                for permission in all_permissions
                if f'{permission.subject}:{permission.action}' in scopes
            ]

            await self._replace_role_permissions(
                role=role,
                permissions=role_permissions,
            )

        admin_user = await self._user_repo.get_by_email(settings.rbac.admin_email)

        if admin_user is None:
            admin_user = User(
                email=settings.rbac.admin_email,
                password_hash=Hasher.get_password_hash(
                    settings.rbac.admin_password,
                ),
            )
            self._role_repo.session.add(admin_user)
            await self._role_repo.session.flush()

        await self._ensure_user_has_role(admin_user, admin_role)
        await self._role_repo.session.commit()
