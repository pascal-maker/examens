from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from database import get_session
from models.birdspotting import BirdSpotting, BirdSpottingCreate, BirdSpottingReadWithBird
from repositories.birdspotting import BirdSpottingRepository

router = APIRouter(prefix="/birdspotting", tags=["Birdspotting"])


def get_birdspotting_repository(session: Annotated[Session, Depends(get_session)]) -> BirdSpottingRepository:
    return BirdSpottingRepository(session)


@router.get("/", response_model=List[BirdSpottingReadWithBird])
async def get_birdspotting(
    repo: Annotated[BirdSpottingRepository, Depends(get_birdspotting_repository)]
):
    return repo.get_all()


@router.get("/{birdspotting_id}", response_model=BirdSpottingReadWithBird)
async def get_one_birdspotting(
    birdspotting_id: int,
    repo: Annotated[BirdSpottingRepository, Depends(get_birdspotting_repository)]
):
    item = repo.get_one(birdspotting_id)
    if not item:
        raise HTTPException(status_code=404, detail="Birdspotting not found")
    return item


@router.post("/", response_model=BirdSpottingReadWithBird, status_code=status.HTTP_201_CREATED)
async def add_birdspotting(
    payload: BirdSpottingCreate,
    repo: Annotated[BirdSpottingRepository, Depends(get_birdspotting_repository)]
):
    return repo.insert(payload)