from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from database import get_session
from models.robot import RobotCreate, RobotReadWithFunctionality, RobotUpdate
from repositories.robot_repository import RobotRepository

router = APIRouter(prefix="/robots", tags=["Robot"])


def get_repo(session: Annotated[Session, Depends(get_session)]) -> RobotRepository:
    return RobotRepository(session)


@router.get("/", response_model=List[RobotReadWithFunctionality])
async def get_all(
    location: Optional[str] = Query(default=None, description="Filter by location"),
    repo: Annotated[RobotRepository, Depends(get_repo)] = None,
):
    return repo.get_all(location=location)


@router.get("/{robot_id}", response_model=RobotReadWithFunctionality)
async def get_one(
    robot_id: int,
    repo: Annotated[RobotRepository, Depends(get_repo)] = None,
):
    item = repo.get_one(robot_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found")
    return item


@router.post("/", response_model=RobotReadWithFunctionality, status_code=status.HTTP_201_CREATED)
async def create(
    payload: RobotCreate,
    repo: Annotated[RobotRepository, Depends(get_repo)] = None,
):
    return repo.insert(payload)


@router.put("/{robot_id}", response_model=RobotReadWithFunctionality)
async def update(
    robot_id: int,
    payload: RobotUpdate,
    repo: Annotated[RobotRepository, Depends(get_repo)] = None,
):
    item = repo.update(robot_id, payload)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found")
    return item


@router.patch("/{robot_id}/functionality/set", response_model=RobotReadWithFunctionality)
async def set_functionality(
    robot_id: int,
    functionality_id: int,
    repo: Annotated[RobotRepository, Depends(get_repo)] = None,
):
    item = repo.set_functionality(robot_id, functionality_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found")
    return item


@router.patch("/{robot_id}/functionality/clear", response_model=RobotReadWithFunctionality)
async def clear_functionality(
    robot_id: int,
    repo: Annotated[RobotRepository, Depends(get_repo)] = None,
):
    item = repo.clear_functionality(robot_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found")
    return item


@router.delete("/{robot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    robot_id: int,
    repo: Annotated[RobotRepository, Depends(get_repo)] = None,
):
    item = repo.delete(robot_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found")
