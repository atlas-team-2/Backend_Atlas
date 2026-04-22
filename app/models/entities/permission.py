from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import BaseModel
from .link_models import RolePermission


class PermissionBase(SQLModel):
    subject: str
    action: str


class Permission(BaseModel, PermissionBase, table=True):
    roles: list["Role"] = Relationship(back_populates="permissions", link_model=RolePermission)


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(SQLModel):
    subject: Optional[str] = None
    action: Optional[str] = None


class PermissionPublic(PermissionBase, BaseModel):
    pass
