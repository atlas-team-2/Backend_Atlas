from pydantic import BaseModel
from typing import Optional
from app.models.models import Gender


class CostumeBase(BaseModel):
    nation_id: str
    gender: Gender
    image_url: str
    description: Optional[str] = None


class CostumeCreate(CostumeBase):
    pass


class CostumeUpdate(BaseModel):
    nation_id: Optional[str] = None
    gender: Optional[Gender] = None
    image_url: Optional[str] = None
    description: Optional[str] = None


class CostumePublic(CostumeBase):
    id: str
