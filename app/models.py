from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

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
    polygon_data: dict
    color: Optional[str] = None

    nation: Nation = Relationship(back_populates="zones")


class NationInfo(SQLModel, table=True):
    id: str = Field(primary_key=True)
    nation_id: str = Field(foreign_key="nation.id")
    origin: Optional[str] = Field(unique=True)
    self_name: str
    language: str
    religion: str
    facts: Optional[str] = None

    nation: Nation = Relationship(back_populates="info")

class Costume(SQLModel, table=True):
    id: str = Field(primary_key=True)
    nation_id: str = Field(foreign_key="nation.id")
    gender: str
    image_url: str
    description: Optional[str] = None
    created_at: datetime

    nation: Nation = Relationship(back_populates="costumes")

class Role(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    description: str
    can_moderate: bool
    can_comment: bool

    users: list["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(unique=True)
    password_hash: str
    created_at: datetime
    role_id: Optional[int] = Field(foreign_key="role.id")

    role: Optional[Role] = Relationship(back_populates="users")
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


class Game(SQLModel, table=True):
    id: str = Field(primary_key=True)
    nation_id: str = Field(foreign_key="nation.id")
    type: str
    title: str
    description: Optional[str] = None
    is_active: bool

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
