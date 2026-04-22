from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import NationRepositoryDep
from app.models.entities.nation import Nation, NationCreate, NationUpdate, NationPublic

class NationService:
    def __init__(self, nation_repository: NationRepositoryDep):
        self.nation_repository = nation_repository

    async def get_nations(self, offset: int = 0, limit: int = 100) -> Sequence[Nation]:
        return await self.nation_repository.fetch(offset=offset, limit=limit)

    async def create_nation(self, nation_create: NationCreate) -> Nation:
        nation = Nation(**nation_create.model_dump())
        return await self.nation_repository.save(nation)

    async def get_nation(self, nation_id: UUID) -> Optional[Nation]:
        return await self.nation_repository.get(nation_id)

    async def update_nation(self, nation_id: UUID, nation_update: NationUpdate) -> Optional[Nation]:
        data = nation_update.model_dump(exclude_unset=True)
        return await self.nation_repository.update(nation_id, data)

    async def delete_nation(self, nation_id: UUID) -> Optional[Nation]:
        return await self.nation_repository.delete(nation_id)
