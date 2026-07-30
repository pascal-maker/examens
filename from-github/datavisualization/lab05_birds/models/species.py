from typing import Optional
from decimal import Decimal
from sqlmodel import SQLModel, Field

class SpeciesBase(SQLModel):
    name: str
    scientific_name: str
    family: str
    conservation_status: str
    wingspan_cm: Decimal = Field(max_digits=5, decimal_places=2)

class Species(SpeciesBase, table=True):
    __tablename__ = "species"
    id: Optional[int] = Field(default=None, primary_key=True)

class SpeciesCreate(SpeciesBase):
    pass

class SpeciesRead(SpeciesBase):
    id: int
