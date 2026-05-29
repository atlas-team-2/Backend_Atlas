from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.responses import auth_responses, detail_responses
from app.dependencies.auth import require_scopes
from app.dependencies.services import CommentServiceDep
from app.models.entities.comment import CommentCreate, CommentPublic, CommentUpdate
from app.schemas.filters import CommonListFilters
from app.utils.errors import NotFoundError

router = APIRouter(
    prefix='/comments',
    tags=['comments'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/')
async def get_comments(
    service: CommentServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[CommentPublic]:
    return await service.get_comments(offset=filters.offset, limit=filters.limit)


@router.post('/')
async def create_comment(
    comment_create: CommentCreate,
    service: CommentServiceDep,
) -> CommentPublic:
    return await service.create_comment(comment_create)


@router.get('/{comment_id}', responses=detail_responses)
async def get_comment(
    comment_id: UUID,
    service: CommentServiceDep,
) -> CommentPublic:
    result = await service.get_comment(comment_id)
    if result is None:
        raise NotFoundError()
    return result


@router.put('/{comment_id}', dependencies=[require_scopes(['comment:update'])], responses={**auth_responses, **detail_responses})
async def update_comment(
    comment_id: UUID,
    comment_update: CommentUpdate,
    service: CommentServiceDep,
) -> CommentPublic:
    result = await service.update_comment(comment_id, comment_update)
    if result is None:
        raise NotFoundError()
    return result


@router.delete('/{comment_id}', dependencies=[require_scopes(['comment:delete'])], responses={**auth_responses, **detail_responses})
async def delete_comment(
    comment_id: UUID,
    service: CommentServiceDep,
) -> CommentPublic:
    result = await service.delete_comment(comment_id)
    if result is None:
        raise NotFoundError()
    return result