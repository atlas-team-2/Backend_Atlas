from typing import Optional, Sequence, TypeVar, Generic
from uuid import UUID

from pydantic import BaseModel as PydanticBaseModel
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies.session import SessionDep
from app.models.base import BaseModel

Model = TypeVar("Model", bound=BaseModel)


class Repository(Generic[Model]):
    def __init__(self, session: SessionDep, model: type[Model]):
        self._session: AsyncSession = session
        self._model: type[Model] = model

    @property
    def model(self) -> type[Model]:
        return self._model

    async def get(self, pk: UUID) -> Optional[Model]:
        return await self._session.get(self.model, pk)

    async def fetch(
        self,
        filters: Optional[PydanticBaseModel] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Sequence[Model]:
        stmt = select(self.model)
        if filters is not None:
            filter_stmt = and_(True)
            for key, value in filters.model_dump().items():
                if hasattr(self.model, key) and value is not None:
                    filter_stmt = and_(filter_stmt, getattr(self.model, key) == value)
            stmt = stmt.where(filter_stmt)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self._session.exec(stmt)
        return result.all()

    async def save(self, instance: Model) -> Model:
        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)
        return instance

    async def save_all(self, instances: list[Model]) -> list[Model]:
        self._session.add_all(instances)
        await self._session.commit()
        for instance in instances:
            await self._session.refresh(instance)
        return instances

    async def delete(self, pk: UUID) -> Optional[Model]:
        instance = await self.get(pk)
        if instance is None:
            return None
        await self._session.delete(instance)
        await self._session.commit()
        return instance

    async def update(self, pk: UUID, updates: PydanticBaseModel) -> Optional[Model]:
        instance = await self.get(pk)
        if instance is None:
            return None
        for key, value in updates.model_dump().items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        await self.save(instance)
        return instance
