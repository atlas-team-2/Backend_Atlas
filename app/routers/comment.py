from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies.services import CommentServiceDep
from app.models.entities.comment import CommentCreate, CommentUpdate, CommentPublic

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)

@router.get("/")
async def get_comments(
    service: CommentServiceDep,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
) -> Sequence[CommentPublic]:
    return await service.get_comments(offset=offset, limit=limit)

@router.post("/")
async def create_comment(
    comment_create: CommentCreate,
    service: CommentServiceDep,
) -> CommentPublic:
    return await service.create_comment(comment_create)

@router.get("/{comment_id}")
async def get_comment(
    comment_id: UUID,
    service: CommentServiceDep,
) -> Optional[CommentPublic]:
    return await service.get_comment(comment_id)

@router.put("/{comment_id}")
async def update_comment(
    comment_id: UUID,
    comment_update: CommentUpdate,
    service: CommentServiceDep,
) -> Optional[CommentPublic]:
    return await service.update_comment(comment_id, comment_update)

@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: UUID,
    service: CommentServiceDep,
) -> Optional[CommentPublic]:
    return await service.delete_comment(comment_id)
