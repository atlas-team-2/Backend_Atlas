from pydantic import BaseModel
from typing import Optional


class NationInfoBase(BaseModel):
    nation_id: str
    origin: str
    self_name: str
    language: list[str]
    religion: list[str]
    facts: Optional[list[str]] = None


class NationInfoCreate(NationInfoBase):
    pass


class NationInfoUpdate(BaseModel):
    nation_id: Optional[str] = None
    origin: Optional[str] = None
    self_name: Optional[str] = None
    language: Optional[list[str]] = None
    religion: Optional[list[str]] = None
    facts: Optional[list[str]] = None


class NationInfoPublic(NationInfoBase):
    id: str
