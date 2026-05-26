from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.responses import auth_responses, detail_responses
from app.dependencies.auth import CurrentUserDep, require_scopes
from app.dependencies.services import UserServiceDep
from app.models.entities.user import UserCreate, UserPublic, UserUpdate
from app.schemas.filters import CommonListFilters
from app.utils.errors import NotFoundError

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['user:read'])], responses=auth_responses)
async def get_users(
    service: UserServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[UserPublic]:
    return await service.get_users(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['user:create'])], responses=auth_responses)
async def create_user(
    user_create: UserCreate,
    service: UserServiceDep,
) -> UserPublic:
    return await service.create_user(user_create.model_dump())


@router.get('/me', dependencies=[require_scopes(['user:read'])], responses=auth_responses)
async def get_me(current_user: CurrentUserDep) -> UserPublic:
    return current_user


@router.get('/{user_id}', dependencies=[require_scopes(['user:read'])], responses={**auth_responses, **detail_responses})
async def get_user(
    user_id: UUID,
    service: UserServiceDep,
) -> UserPublic:
    result = await service.get_user(user_id)
    if result is None:
        raise NotFoundError()
    return result


@router.put('/{user_id}', dependencies=[require_scopes(['user:update'])], responses={**auth_responses, **detail_responses})
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    service: UserServiceDep,
) -> UserPublic:
    result = await service.update_user(user_id, user_update)
    if result is None:
        raise NotFoundError()
    return result


@router.delete('/{user_id}', dependencies=[require_scopes(['user:delete'])], responses={**auth_responses, **detail_responses})
async def delete_user(
    service: UserServiceDep,
    user_id: UUID,
) -> UserPublic:
    result = await service.delete_user(user_id)
    if result is None:
        raise NotFoundError()
    return result


@router.post('/{user_id}/roles/{role_id}', dependencies=[require_scopes(['user:update'])], responses={**auth_responses, **detail_responses})
async def assign_role(
    user_id: UUID,
    role_id: UUID,
    service: UserServiceDep,
) -> UserPublic:
    result = await service.assign_role(user_id, role_id)
    if result is None:
        raise NotFoundError()
    return result


@router.delete('/{user_id}/roles/{role_id}', dependencies=[require_scopes(['user:update'])], responses={**auth_responses, **detail_responses})
async def revoke_role(
    user_id: UUID,
    role_id: UUID,
    service: UserServiceDep,
) -> UserPublic:
    result = await service.revoke_role(user_id, role_id)
    if result is None:
        raise NotFoundError()
    return result