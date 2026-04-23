from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import BaseModel
from .link_models import RolePermission, UserRole


class RoleBase(SQLModel):
    name: str = Field(unique=True)
    description: str


class Role(BaseModel, RoleBase, table=True):
    permissions: list["Permission"] = Relationship(back_populates="roles", link_model=RolePermission)
    users: list["User"] = Relationship(back_populates="roles", link_model=UserRole)


class RoleCreate(RoleBase):
    pass


class RoleUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class RolePublic(RoleBase, BaseModel):
    pass
