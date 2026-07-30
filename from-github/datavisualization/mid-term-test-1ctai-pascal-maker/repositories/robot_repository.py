from typing import Optional
from sqlmodel import Session, select
from fastapi import HTTPException, status

from models.robot import Robot, RobotCreate, RobotUpdate
from models.functionality import Functionality


class RobotRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, location: Optional[str] = None):
        statement = select(Robot)
        if location:
            statement = statement.where(Robot.location == location)
        return self.session.exec(statement).all()

    def get_one(self, robot_id: int):
        return self.session.get(Robot, robot_id)

    def insert(self, payload: RobotCreate):
        if payload.ip_address:
            clash = self.session.exec(
                select(Robot).where(Robot.ip_address == payload.ip_address)
            ).first()
            if clash:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"IP address '{payload.ip_address}' is already used by another robot",
                )
        if payload.current_functionality_id:
            func = self.session.get(Functionality, payload.current_functionality_id)
            if not func:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Functionality {payload.current_functionality_id} not found",
                )
        item = Robot.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def update(self, robot_id: int, payload: RobotUpdate):
        item = self.session.get(Robot, robot_id)
        if not item:
            return None
        if payload.ip_address is not None:
            clash = self.session.exec(
                select(Robot).where(
                    Robot.ip_address == payload.ip_address,
                    Robot.id != robot_id,
                )
            ).first()
            if clash:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"IP address '{payload.ip_address}' is already used by another robot",
                )
        if payload.current_functionality_id is not None:
            func = self.session.get(Functionality, payload.current_functionality_id)
            if not func:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Functionality {payload.current_functionality_id} not found",
                )
        data = payload.model_dump(exclude_unset=True)
        item.sqlmodel_update(data)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def set_functionality(self, robot_id: int, functionality_id: Optional[int]):
        item = self.session.get(Robot, robot_id)
        if not item:
            return None
        if functionality_id is not None:
            func = self.session.get(Functionality, functionality_id)
            if not func:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Functionality {functionality_id} not found",
                )
        item.current_functionality_id = functionality_id
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def clear_functionality(self, robot_id: int):
        return self.set_functionality(robot_id, None)

    def delete(self, robot_id: int):
        item = self.session.get(Robot, robot_id)
        if not item:
            return None
        self.session.delete(item)
        self.session.commit()
        return item
