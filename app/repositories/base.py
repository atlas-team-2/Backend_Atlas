from typing import Generic, Optional, Sequence, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

ModelType = TypeVar('ModelType', bound=SQLModel)


class Repository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self._session = session
        self._model = model

    async def get(self, item_id: UUID) -> Optional[ModelType]:
        return await self._session.get(self._model, item_id)

    async def fetch(
        self,
        offset: int = 0,
        limit: int = 100,
        filters: dict | None = None,
    ) -> Sequence[ModelType]:
        stmt = select(self._model)

        if filters:
            for field_name, value in filters.items():
                stmt = stmt.where(getattr(self._model, field_name) == value)

        stmt = stmt.offset(offset).limit(limit)

        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def fetch_one(
        self,
        filters: dict,
    ) -> Optional[ModelType]:
        stmt = select(self._model)

        for field_name, value in filters.items():
            stmt = stmt.where(getattr(self._model, field_name) == value)

        result = await self._session.execute(stmt)

        return result.scalars().first()

    async def save(self, instance: ModelType) -> ModelType:
        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)

        return instance

    async def update(
        self,
        item_id: UUID,
        data: dict,
    ) -> Optional[ModelType]:
        instance = await self.get(item_id)

        if instance is None:
            return None

        for key, value in data.items():
            setattr(instance, key, value)

        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)

        return instance

    async def delete(self, item_id: UUID) -> Optional[ModelType]:
        instance = await self.get(item_id)

        if instance is None:
            return None

        await self._session.delete(instance)
        await self._session.commit()

        return instance
