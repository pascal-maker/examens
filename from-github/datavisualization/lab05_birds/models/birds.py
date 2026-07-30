from typing import Optional
from sqlmodel import SQLModel,Field,Relationship
from models.species import Species, SpeciesRead

class BirdBase(SQLModel):
    nickname:str
    ring_code:str
    age: int = Field(ge=0)

class Bird(BirdBase,table=True):
    __tablename__ = "birds"
    id: Optional[int] = Field(default=None,primary_key=True)
    species_id: int = Field(foreign_key="species.id", ondelete="RESTRICT")
    species: Optional[Species] = Relationship()    

class BirdCreate(BirdBase):
    species_id:int

class BirdRead(BirdBase):
    id: int
    species_id: int

class BirdReadWithSpecies(BirdRead):
    species: Optional[SpeciesRead] = None

