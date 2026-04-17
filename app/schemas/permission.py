from pydantic import BaseModel
from typing import Optional


class PermissionBase(BaseModel):
    subject: str
    action: str


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    subject: Optional[str] = None
    action: Optional[str] = None


class PermissionPublic(PermissionBase):
    id: int
