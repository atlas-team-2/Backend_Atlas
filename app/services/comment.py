from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import CommentRepositoryDep
from app.models.entities.comment import Comment, CommentCreate, CommentUpdate, CommentPublic

class CommentService:
    def __init__(self, comment_repository: CommentRepositoryDep):
        self.comment_repository = comment_repository

    async def get_comments(self, offset: int = 0, limit: int = 100) -> Sequence[Comment]:
        return await self.comment_repository.fetch(offset=offset, limit=limit)

    async def create_comment(self, comment_create: CommentCreate) -> Comment:
        comment = Comment(**comment_create.model_dump(), is_approved=False)
        return await self.comment_repository.save(comment)

    async def get_comment(self, comment_id: UUID) -> Optional[Comment]:
        return await self.comment_repository.get(comment_id)

    async def update_comment(self, comment_id: UUID, comment_update: CommentUpdate) -> Optional[Comment]:
        data = comment_update.model_dump(exclude_unset=True)
        return await self.comment_repository.update(comment_id, data)

    async def delete_comment(self, comment_id: UUID) -> Optional[Comment]:
        return await self.comment_repository.delete(comment_id)
