from app.models.entities.permission import Permission
from app.repositories.base import Repository

class PermissionRepository(Repository[Permission]):
    def __init__(self, session):
        super().__init__(session, Permission)
