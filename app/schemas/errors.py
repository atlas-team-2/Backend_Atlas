from typing import Optional

from pydantic import PrivateAttr
from sqlmodel import Field, SQLModel

from app.utils.errors import (
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
)


class ErrorSchema(SQLModel):
    detail: Optional[dict] = Field(default_factory=dict)
    message: str
    _error_cls: type[Exception] = PrivateAttr(default=Exception)

    @property
    def error_cls(self) -> type[Exception]:
        return self._error_cls


class NotFoundErrorSchema(ErrorSchema):
    _error_cls: type[Exception] = PrivateAttr(default=NotFoundError)
    message: str = NotFoundError.message


class InternalServerErrorSchema(ErrorSchema):
    _error_cls: type[Exception] = PrivateAttr(default=InternalServerError)
    message: str = InternalServerError.message


class ForbiddenErrorSchema(ErrorSchema):
    _error_cls: type[Exception] = PrivateAttr(default=ForbiddenError)
    message: str = ForbiddenError.message


class UnauthorizedErrorSchema(ErrorSchema):
    _error_cls: type[Exception] = PrivateAttr(default=UnauthorizedError)
    message: str = UnauthorizedError.message