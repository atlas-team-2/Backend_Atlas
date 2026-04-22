from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import GameQuestionRepositoryDep
from app.models.entities.game_question import GameQuestion, GameQuestionCreate, GameQuestionUpdate, GameQuestionPublic

class GameQuestionService:
    def __init__(self, game_question_repository: GameQuestionRepositoryDep):
        self.game_question_repository = game_question_repository

    async def get_game_questions(self, offset: int = 0, limit: int = 100) -> Sequence[GameQuestion]:
        return await self.game_question_repository.fetch(offset=offset, limit=limit)

    async def create_game_question(self, game_question_create: GameQuestionCreate) -> GameQuestion:
        game_question = GameQuestion(**game_question_create.model_dump())
        return await self.game_question_repository.save(game_question)

    async def get_game_question(self, game_question_id: UUID) -> Optional[GameQuestion]:
        return await self.game_question_repository.get(game_question_id)

    async def update_game_question(self, game_question_id: UUID, game_question_update: GameQuestionUpdate) -> Optional[GameQuestion]:
        data = game_question_update.model_dump(exclude_unset=True)
        return await self.game_question_repository.update(game_question_id, data)

    async def delete_game_question(self, game_question_id: UUID) -> Optional[GameQuestion]:
        return await self.game_question_repository.delete(game_question_id)
