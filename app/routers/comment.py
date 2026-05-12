from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.auth import require_scopes
from app.dependencies.services import CommentServiceDep
from app.models.entities.comment import CommentCreate, CommentPublic, CommentUpdate
from app.schemas.filters import CommonListFilters

router = APIRouter(
    prefix='/comments',
    tags=['comments'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['comment:read'])])
async def get_comments(
    service: CommentServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[CommentPublic]:
    return await service.get_comments(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['comment:create'])])
async def create_comment(
    comment_create: CommentCreate,
    service: CommentServiceDep,
) -> CommentPublic:
    return await service.create_comment(comment_create)


@router.get('/{comment_id}', dependencies=[require_scopes(['comment:read'])])
async def get_comment(
    comment_id: UUID,
    service: CommentServiceDep,
) -> Optional[CommentPublic]:
    return await service.get_comment(comment_id)


@router.put('/{comment_id}', dependencies=[require_scopes(['comment:update'])])
async def update_comment(
    comment_id: UUID,
    comment_update: CommentUpdate,
    service: CommentServiceDep,
) -> Optional[CommentPublic]:
    return await service.update_comment(comment_id, comment_update)


@router.delete('/{comment_id}', dependencies=[require_scopes(['comment:delete'])])
async def delete_comment(
    comment_id: UUID,
    service: CommentServiceDep,
) -> Optional[CommentPublic]:
    return await service.delete_comment(comment_id)
