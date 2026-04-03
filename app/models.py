from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import EmailStr

class Nation(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str = Field(index=True, unique=True)
    slug: str = Field(index=True, unique=True)
    population: Optional[int] = None
    image_url: Optional[str] = None

    info: Optional["NationInfo"] = Relationship(back_populates="nation")
    zones: list["SettlementZone"] = Relationship(back_populates="nation")
    costumes: list["Costume"] = Relationship(back_populates="nation")
    comments: list["Comment"] = Relationship(back_populates="nation")
    games: list["Game"] = Relationship(back_populates="nation")


class SettlementZone(SQLModel, table=True):
    id: str = Field(primary_key=True)
    nation_id: str = Field(foreign_key="nation.id")
    region_name: str
    polygon_data: list
    color: Optional[str] = None

    nation: Nation = Relationship(back_populates="zones")


class NationInfo(SQLModel, table=True):
    id: str = Field(primary_key=True)
    nation_id: str = Field(foreign_key="nation.id")
    origin: str
    self_name: str
    language: List[str]
    religion: List[str]
    facts: Optional[List[str]] = None

    nation: Nation = Relationship(back_populates="info")


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Costume(SQLModel, table=True):
    id: str = Field(primary_key=True)
    nation_id: str = Field(foreign_key="nation.id")
    gender: Gender
    image_url: str
    description: Optional[str] = None
    created_at: datetime

    nation: Nation = Relationship(back_populates="costumes")


class Permission(SQLModel, table=True):
    id: int = Field(primary_key=True)
    subject: str
    action: str

    roles: list["Role"] = Relationship(
        back_populates="permissions",
        link_model="RolePermission"
    )

class RolePermission(SQLModel, table=True):
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)

class UserRole(SQLModel, table=True):
    user_id: str = Field(foreign_key="user.id", primary_key=True)
    role_id: int = Field(foreign_key="role.id", primary_key=True)


class Role(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    description: str

    permissions: list["Permission"] = Relationship(
        back_populates="roles",
        link_model=RolePermission
    )

    users: list["User"] = Relationship(
        back_populates="roles",
        link_model=UserRole
    )


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: EmailStr = Field(unique=True)
    password_hash: str
    created_at: datetime

    roles: list["Role"] = Relationship(
        back_populates="users",
        link_model=UserRole
    )

    comments: list["Comment"] = Relationship(back_populates="user")


class Comment(SQLModel, table=True):
    id: str = Field(primary_key=True)
    nation_id: str = Field(foreign_key="nation.id")
    user_id: str = Field(foreign_key="user.id")
    text: str
    created_at: datetime
    is_approved: bool

    nation: Nation = Relationship(back_populates="comments")
    user: User = Relationship(back_populates="comments")


class GameType(str, Enum):
    dish = "dish"
    holiday = "holiday"
    ornament = "ornament"


class Game(SQLModel, table=True):
    id: str = Field(primary_key=True)
    nation_id: str = Field(foreign_key="nation.id")
    type: GameType
    title: str
    description: Optional[str] = None

    nation: Nation = Relationship(back_populates="games")
    questions: list["GameQuestion"] = Relationship(back_populates="game")


class GameQuestion(SQLModel, table=True):
    id: str = Field(primary_key=True)
    game_id: str = Field(foreign_key="game.id")
    question_text: str
    image_url: Optional[str] = None
    order_index: int

    game: Game = Relationship(back_populates="questions")
    options: list["GameOption"] = Relationship(back_populates="question")


class GameOption(SQLModel, table=True):
    id: str = Field(primary_key=True)
    question_id: str = Field(foreign_key="gamequestion.id")
    text: str
    is_correct: bool
    image_url: Optional[str] = None
    explanation: Optional[str] = None

    question: GameQuestion = Relationship(back_populates="options")
