import math
from typing import Generic, Optional, Sequence, TypeVar
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

from app.schemas.filters import CommonListFilters
from app.utils.pagination import ListResponse, PaginationInfo

ModelType = TypeVar('ModelType', bound=SQLModel)


class Repository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self._session = session
        self._model = model

    @property
    def session(self) -> AsyncSession:
        return self._session

    async def get(self, item_id: UUID) -> Optional[ModelType]:
        return await self._session.get(self._model, item_id)

    def _apply_filters(self, stmt, filters: dict | None = None):
        if not filters:
            return stmt

        for field_name, value in filters.items():
            if value is None:
                continue
            stmt = stmt.where(getattr(self._model, field_name) == value)

        return stmt

    async def fetch(
        self,
        offset: int = 0,
        limit: int = 100,
        filters: dict | None = None,
    ) -> Sequence[ModelType]:
        stmt = select(self._model)
        stmt = self._apply_filters(stmt, filters)
        stmt = stmt.offset(offset).limit(limit)

        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def fetch_with_pagination_data(
        self,
        filters: CommonListFilters,
    ) -> ListResponse[ModelType]:
        query_filters = filters.model_dump(
            exclude={'offset', 'limit'},
            exclude_none=True,
        )

        limit = filters.limit
        offset = filters.offset

        select_statement = self._apply_filters(
            select(self._model),
            query_filters,
        )

        count_statement = self._apply_filters(
            select(func.count()).select_from(self._model),
            query_filters,
        )

        total = (await self._session.execute(count_statement)).scalar_one()

        result = await self._session.execute(
            select_statement.limit(limit).offset(offset),
        )
        items = list(result.scalars().all())

        pages_num = math.ceil(total / limit) if total else 0
        page = (offset // limit) + 1

        return ListResponse(
            info=PaginationInfo(
                page=page,
                pages_num=pages_num,
                total=total,
            ),
            items=items,
        )

    async def fetch_one(
        self,
        filters: dict,
    ) -> Optional[ModelType]:
        stmt = select(self._model)
        stmt = self._apply_filters(stmt, filters)

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
