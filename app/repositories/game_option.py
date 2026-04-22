from app.models.entities.game_option import GameOption
from app.repositories.base import Repository

class GameOptionRepository(Repository[GameOption]):
    def __init__(self, session):
        super().__init__(session, GameOption)
