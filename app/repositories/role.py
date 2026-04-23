from app.models.entities.role import Role
from app.repositories.base import Repository

class RoleRepository(Repository[Role]):
    def __init__(self, session):
        super().__init__(session, Role)
