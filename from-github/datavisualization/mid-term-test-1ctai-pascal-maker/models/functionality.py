from typing import Optional
from sqlmodel import SQLModel, Field


class FunctionalityBase(SQLModel):
    name: str = Field(min_length=1, unique=True)
    description: Optional[str] = None


class Functionality(FunctionalityBase, table=True):
    __tablename__ = "functionalities"
    id: Optional[int] = Field(default=None, primary_key=True)


class FunctionalityCreate(FunctionalityBase):
    pass


class FunctionalityUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = None


class FunctionalityRead(FunctionalityBase):
    id: int
