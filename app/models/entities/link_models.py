from sqlmodel import SQLModel, Field
from uuid import UUID


class RolePermission(SQLModel, table=True):
    role_id: UUID = Field(foreign_key="role.id", primary_key=True)
    permission_id: UUID = Field(foreign_key="permission.id", primary_key=True)


class UserRole(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    role_id: UUID = Field(foreign_key="role.id", primary_key=True)
