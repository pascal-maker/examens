from typing import Annotated,List
from fastapi import APIRouter,Depends,HTTPException,status
from sqlmodel import Session
from database import get_session

from models.birds import Bird, BirdCreate, BirdReadWithSpecies
from repositories.birds import BirdRepository

router = APIRouter(prefix="/birds",tags=["Birds"])
def get_bird_repository(session: Annotated[Session,Depends(get_session)],) -> BirdRepository:
    return BirdRepository(session)
    
@router.get("/", response_model=List[BirdReadWithSpecies])
async def get_birds(
    repo: Annotated[BirdRepository, Depends(get_bird_repository)]
):
    return repo.get_all()

@router.get("/{bird_id}", response_model=BirdReadWithSpecies)
async def get_one_bird(
    bird_id:int,
    repo: Annotated[BirdRepository, Depends(get_bird_repository)]
):  
    item = repo.get_one(bird_id)
    if not item:
        raise HTTPException(status_code=404,detail="Bird not found")
    return item

@router.post("/", response_model=BirdReadWithSpecies, status_code=status.HTTP_201_CREATED)
async def create_bird(
    payload:BirdCreate,
    repo: Annotated[BirdRepository, Depends(get_bird_repository)]
):
    return repo.insert(payload)