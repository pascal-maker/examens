from sqlmodel import Session, select
from fastapi import HTTPException, status

from models.functionality import Functionality, FunctionalityCreate, FunctionalityUpdate


class FunctionalityRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.exec(select(Functionality)).all()

    def get_one(self, functionality_id: int):
        return self.session.get(Functionality, functionality_id)

    def insert(self, payload: FunctionalityCreate):
        existing = self.session.exec(
            select(Functionality).where(Functionality.name == payload.name)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A functionality named '{payload.name}' already exists",
            )
        item = Functionality.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def update(self, functionality_id: int, payload: FunctionalityUpdate):
        item = self.session.get(Functionality, functionality_id)
        if not item:
            return None
        if payload.name is not None:
            clash = self.session.exec(
                select(Functionality).where(
                    Functionality.name == payload.name,
                    Functionality.id != functionality_id,
                )
            ).first()
            if clash:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"A functionality named '{payload.name}' already exists",
                )
        data = payload.model_dump(exclude_unset=True)
        item.sqlmodel_update(data)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, functionality_id: int):
        item = self.session.get(Functionality, functionality_id)
        if not item:
            return None
        self.session.delete(item)
        self.session.commit()
        return item
