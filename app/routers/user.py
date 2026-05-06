from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.auth import CurrentUserDep
from app.dependencies.services import UserServiceDep
from app.models.entities.user import UserCreate, UserPublic, UserUpdate
from app.schemas.filters import CommonListFilters

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/')
async def get_users(
    service: UserServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[UserPublic]:
    return await service.get_users(offset=filters.offset, limit=filters.limit)


@router.post('/')
async def create_user(
    user_create: UserCreate,
    service: UserServiceDep,
) -> UserPublic:
    return await service.create_user(user_create)


@router.get('/me')
async def get_me(current_user: CurrentUserDep) -> UserPublic:
    return current_user


@router.get('/{user_id}')
async def get_user(
    user_id: UUID,
    service: UserServiceDep,
) -> Optional[UserPublic]:
    return await service.get_user(user_id)


@router.put('/{user_id}')
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    service: UserServiceDep,
) -> Optional[UserPublic]:
    return await service.update_user(user_id, user_update)


@router.delete('/{user_id}')
async def delete_user(
    user_id: UUID,
    service: UserServiceDep,
) -> Optional[UserPublic]:
    return await service.delete_user(user_id)
