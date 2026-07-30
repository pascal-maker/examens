from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from database import get_session
from models.species import Species, SpeciesCreate
from repositories.species import SpeciesRepository

router = APIRouter(prefix="/species", tags=["Species"])

def get_species_repository(session: Annotated[Session, Depends(get_session)]) -> SpeciesRepository:
    return SpeciesRepository(session)

@router.get("/", response_model=List[Species])
async def get_all_species(
    repo: Annotated[SpeciesRepository, Depends(get_species_repository)]
):
    return repo.get_all()

@router.post("/", response_model=Species, status_code=status.HTTP_201_CREATED)
async def create_species(
    payload: SpeciesCreate,
    repo: Annotated[SpeciesRepository, Depends(get_species_repository)]
):
    return repo.insert(payload)
