from app.core.rbac import PERMISSIONS_MAP
from app.core.security import OAUTH2_SCOPES
from app.core.settings import settings
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
        perm = await self._perm_repo.get_by_scope(subject, action)
        if perm is None:
            perm = await self._perm_repo.save(Permission(subject=subject, action=action))
        return perm

    async def bootstrap(self) -> None:
        all_permissions: list[Permission] = []
        for scope in OAUTH2_SCOPES:
            if scope == 'refresh':
                continue
            subject, action = scope.split(':', 1)
            perm = await self._get_or_create_permission(subject, action)
            all_permissions.append(perm)

        admin_role = await self._role_repo.get_by_name_with_permissions(
            settings.rbac.admin_role
        )
        if admin_role is None:
            admin_role = Role(
                name=settings.rbac.admin_role,
                description='Administrator with full access',
            )
            self._role_repo._session.add(admin_role)
            await self._role_repo._session.flush()
        admin_role.permissions = all_permissions
        await self._role_repo._session.commit()

        for role_name, scopes in PERMISSIONS_MAP.items():
            role = await self._role_repo.get_by_name_with_permissions(role_name)
            if role is None:
                role = Role(name=role_name, description=f'{role_name.capitalize()} role')
                self._role_repo._session.add(role)
                await self._role_repo._session.flush()
            role.permissions = [
                p for p in all_permissions if f'{p.subject}:{p.action}' in scopes
            ]
            await self._role_repo._session.commit()

        admin_user = await self._user_repo.get_by_email(settings.rbac.admin_email)
        if admin_user is None:
            admin_role = await self._role_repo.get_by_name(settings.rbac.admin_role)
            admin_user = User(
                email=settings.rbac.admin_email,
                password_hash=Hasher.get_password_hash(settings.rbac.admin_password),
            )
            self._role_repo._session.add(admin_user)
            await self._role_repo._session.flush()
            admin_user.roles = [admin_role]
            await self._role_repo._session.commit()
