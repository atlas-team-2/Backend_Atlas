from app.models.entities.costume import Costume
from app.repositories.base import Repository

class CostumeRepository(Repository[Costume]):
    def __init__(self, session):
        super().__init__(session, Costume)
