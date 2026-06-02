from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlmodel import SQLModel

T = TypeVar('T', bound=SQLModel)


class PaginationInfo(SQLModel):
    page: int
    pages_num: int
    total: int


class ListResponse(BaseModel, Generic[T]):
    info: PaginationInfo
    items: list[T]
