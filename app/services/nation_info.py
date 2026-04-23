from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import NationInfoRepositoryDep
from app.models.entities.nation_info import NationInfo, NationInfoCreate, NationInfoUpdate, NationInfoPublic

class NationInfoService:
    def __init__(self, nation_info_repository: NationInfoRepositoryDep):
        self.nation_info_repository = nation_info_repository

    async def get_nation_infos(self, offset: int = 0, limit: int = 100) -> Sequence[NationInfo]:
        return await self.nation_info_repository.fetch(offset=offset, limit=limit)

    async def create_nation_info(self, nation_info_create: NationInfoCreate) -> NationInfo:
        info = NationInfo(**nation_info_create.model_dump())
        return await self.nation_info_repository.save(info)

    async def get_nation_info(self, info_id: UUID) -> Optional[NationInfo]:
        return await self.nation_info_repository.get(info_id)

    async def update_nation_info(self, info_id: UUID, nation_info_update: NationInfoUpdate) -> Optional[NationInfo]:
        data = nation_info_update.model_dump(exclude_unset=True)
        return await self.nation_info_repository.update(info_id, data)

    async def delete_nation_info(self, info_id: UUID) -> Optional[NationInfo]:
        return await self.nation_info_repository.delete(info_id)
