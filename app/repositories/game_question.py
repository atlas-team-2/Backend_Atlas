from app.models.entities.game_question import GameQuestion
from app.repositories.base import Repository

class GameQuestionRepository(Repository[GameQuestion]):
    def __init__(self, session):
        super().__init__(session, GameQuestion)
