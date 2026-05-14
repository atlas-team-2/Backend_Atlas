from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.auth import CurrentUserDep, require_scopes
from app.dependencies.services import UserServiceDep
from app.models.entities.user import UserCreate, UserPublic, UserUpdate
from app.schemas.filters import CommonListFilters

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['user:read'])])
async def get_users(
    service: UserServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[UserPublic]:
    return await service.get_users(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['user:create'])])
async def create_user(
    user_create: UserCreate,
    service: UserServiceDep,
) -> UserPublic:
    return await service.create_user(user_create.model_dump())


@router.get('/me', dependencies=[require_scopes(['user:read'])])
async def get_me(current_user: CurrentUserDep) -> UserPublic:
    return current_user


@router.get('/{user_id}', dependencies=[require_scopes(['user:read'])])
async def get_user(
    user_id: UUID,
    service: UserServiceDep,
) -> Optional[UserPublic]:
    return await service.get_user(user_id)


@router.put('/{user_id}', dependencies=[require_scopes(['user:update'])])
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    service: UserServiceDep,
) -> Optional[UserPublic]:
    return await service.update_user(user_id, user_update)


@router.delete('/{user_id}', dependencies=[require_scopes(['user:delete'])])
async def delete_user(
    service: UserServiceDep,
    user_id: UUID,
) -> Optional[UserPublic]:
    return await service.delete_user(user_id)


@router.post('/{user_id}/roles/{role_id}', dependencies=[require_scopes(['user:update'])])
async def assign_role(
    user_id: UUID,
    role_id: UUID,
    service: UserServiceDep,
) -> Optional[UserPublic]:
    return await service.assign_role(user_id, role_id)


@router.delete('/{user_id}/roles/{role_id}', dependencies=[require_scopes(['user:update'])])
async def revoke_role(
    user_id: UUID,
    role_id: UUID,
    service: UserServiceDep,
) -> Optional[UserPublic]:
    return await service.revoke_role(user_id, role_id)
