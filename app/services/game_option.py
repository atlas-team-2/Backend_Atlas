from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import GameOptionRepositoryDep
from app.models.entities.game_option import GameOption, GameOptionCreate, GameOptionUpdate, GameOptionPublic

class GameOptionService:
    def __init__(self, game_option_repository: GameOptionRepositoryDep):
        self.game_option_repository = game_option_repository

    async def get_game_options(self, offset: int = 0, limit: int = 100) -> Sequence[GameOption]:
        return await self.game_option_repository.fetch(offset=offset, limit=limit)

    async def create_game_option(self, game_option_create: GameOptionCreate) -> GameOption:
        game_option = GameOption(**game_option_create.model_dump())
        return await self.game_option_repository.save(game_option)

    async def get_game_option(self, game_option_id: UUID) -> Optional[GameOption]:
        return await self.game_option_repository.get(game_option_id)

    async def update_game_option(self, game_option_id: UUID, game_option_update: GameOptionUpdate) -> Optional[GameOption]:
        data = game_option_update.model_dump(exclude_unset=True)
        return await self.game_option_repository.update(game_option_id, data)

    async def delete_game_option(self, game_option_id: UUID) -> Optional[GameOption]:
        return await self.game_option_repository.delete(game_option_id)
