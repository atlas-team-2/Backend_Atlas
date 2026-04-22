from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import GameRepositoryDep
from app.models.entities.game import Game, GameCreate, GameUpdate, GamePublic

class GameService:
    def __init__(self, game_repository: GameRepositoryDep):
        self.game_repository = game_repository

    async def get_games(self, offset: int = 0, limit: int = 100) -> Sequence[Game]:
        return await self.game_repository.fetch(offset=offset, limit=limit)

    async def create_game(self, game_create: GameCreate) -> Game:
        game = Game(**game_create.model_dump())
        return await self.game_repository.save(game)

    async def get_game(self, game_id: UUID) -> Optional[Game]:
        return await self.game_repository.get(game_id)

    async def update_game(self, game_id: UUID, game_update: GameUpdate) -> Optional[Game]:
        data = game_update.model_dump(exclude_unset=True)
        return await self.game_repository.update(game_id, data)

    async def delete_game(self, game_id: UUID) -> Optional[Game]:
        return await self.game_repository.delete(game_id)
