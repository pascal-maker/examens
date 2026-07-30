from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel,Field,Relationship
from models.birds import Bird, BirdRead

class BirdSpottingBase(SQLModel):
    spotted_at:datetime = Field(default_factory=datetime.now)
    location:str
    observer_name:str
    notes:Optional[str] = None

class BirdSpotting(BirdSpottingBase,table=True):
    __tablename__ = "birdspotting"
    id: Optional[int] = Field(default=None,primary_key=True)
    bird_id: int = Field(foreign_key="birds.id", ondelete="CASCADE")
    bird: Optional[Bird] = Relationship()

class BirdSpottingCreate(BirdSpottingBase):
    bird_id:int

class BirdSpottingRead(BirdSpottingBase):
    id: int
    bird_id: int

class BirdSpottingReadWithBird(BirdSpottingRead):
    bird: Optional[BirdRead] = None