from app.models.entities.user import User
from app.repositories.base import Repository

class UserRepository(Repository[User]):
    def __init__(self, session):
        super().__init__(session, User)
