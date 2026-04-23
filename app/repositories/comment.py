from app.models.entities.comment import Comment
from app.repositories.base import Repository

class CommentRepository(Repository[Comment]):
    def __init__(self, session):
        super().__init__(session, Comment)
