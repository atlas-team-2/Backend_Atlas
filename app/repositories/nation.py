from app.models.entities.nation import Nation
from app.repositories.base import Repository

class NationRepository(Repository[Nation]):
    def __init__(self, session):
        super().__init__(session, Nation)
