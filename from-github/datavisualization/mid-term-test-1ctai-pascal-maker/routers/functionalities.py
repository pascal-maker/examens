from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from database import get_session
from models.functionality import FunctionalityCreate, FunctionalityRead, FunctionalityUpdate
from repositories.functionality_repository import FunctionalityRepository

router = APIRouter(prefix="/functionalities", tags=["Functionality"])


def get_repo(session: Annotated[Session, Depends(get_session)]) -> FunctionalityRepository:
    return FunctionalityRepository(session)


@router.get("/", response_model=List[FunctionalityRead])
async def get_all(repo: Annotated[FunctionalityRepository, Depends(get_repo)] = None):
    return repo.get_all()


@router.get("/{functionality_id}", response_model=FunctionalityRead)
async def get_one(
    functionality_id: int,
    repo: Annotated[FunctionalityRepository, Depends(get_repo)] = None,
):
    item = repo.get_one(functionality_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Functionality not found")
    return item


@router.post("/", response_model=FunctionalityRead, status_code=status.HTTP_201_CREATED)
async def create(
    payload: FunctionalityCreate,
    repo: Annotated[FunctionalityRepository, Depends(get_repo)] = None,
):
    return repo.insert(payload)


@router.put("/{functionality_id}", response_model=FunctionalityRead)
async def update(
    functionality_id: int,
    payload: FunctionalityUpdate,
    repo: Annotated[FunctionalityRepository, Depends(get_repo)] = None,
):
    item = repo.update(functionality_id, payload)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Functionality not found")
    return item


@router.delete("/{functionality_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    functionality_id: int,
    repo: Annotated[FunctionalityRepository, Depends(get_repo)] = None,
):
    item = repo.delete(functionality_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Functionality not found")
