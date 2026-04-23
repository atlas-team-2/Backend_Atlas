from app.models.entities.game import Game
from app.repositories.base import Repository

class GameRepository(Repository[Game]):
    def __init__(self, session):
        super().__init__(session, Game)
