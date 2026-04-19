from pydantic import BaseModel
from typing import Optional


class NationBase(BaseModel):
    name: str
    slug: str
    population: Optional[int] = None
    image_url: Optional[str] = None


class NationCreate(NationBase):
    pass


class NationUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    population: Optional[int] = None
    image_url: Optional[str] = None


class NationPublic(NationBase):
    id: str
