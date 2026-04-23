from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import CostumeRepositoryDep
from app.models.entities.costume import Costume, CostumeCreate, CostumeUpdate, CostumePublic

class CostumeService:
    def __init__(self, costume_repository: CostumeRepositoryDep):
        self.costume_repository = costume_repository

    async def get_costumes(self, offset: int = 0, limit: int = 100) -> Sequence[Costume]:
        return await self.costume_repository.fetch(offset=offset, limit=limit)

    async def create_costume(self, costume_create: CostumeCreate) -> Costume:
        costume = Costume(**costume_create.model_dump())
        return await self.costume_repository.save(costume)

    async def get_costume(self, costume_id: UUID) -> Optional[Costume]:
        return await self.costume_repository.get(costume_id)

    async def update_costume(self, costume_id: UUID, costume_update: CostumeUpdate) -> Optional[Costume]:
        data = costume_update.model_dump(exclude_unset=True)
        return await self.costume_repository.update(costume_id, data)

    async def delete_costume(self, costume_id: UUID) -> Optional[Costume]:
        return await self.costume_repository.delete(costume_id)
