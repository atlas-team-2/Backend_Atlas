from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies.services import UserServiceDep
from app.models.entities.user import UserCreate, UserUpdate, UserPublic

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
async def get_users(
    service: UserServiceDep,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
) -> Sequence[UserPublic]:
    return await service.get_users(offset=offset, limit=limit)


@router.post("/")
async def create_user(
    user_create: UserCreate,
    service: UserServiceDep,
) -> UserPublic:
    return await service.create_user(user_create)


@router.get("/{user_id}")
async def get_user(
    user_id: UUID,
    service: UserServiceDep,
) -> Optional[UserPublic]:
    return await service.get_user(user_id)


@router.put("/{user_id}")
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    service: UserServiceDep,
) -> Optional[UserPublic]:
    return await service.update_user(user_id, user_update)


@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    service: UserServiceDep,
) -> Optional[UserPublic]:
    return await service.delete_user(user_id)
