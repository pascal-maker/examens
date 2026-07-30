from sqlmodel import Session,select
from fastapi import HTTPException
from models.birds import Bird,BirdCreate
from models.species import Species


class BirdRepository:
    def __init__(self,session:Session):
        self.session = session

    def get_all(self):
        statement = select(Bird)
        return self.session.exec(statement).all()

    def get_one(self,bird_id:int):
        return self.session.get(Bird,bird_id)
    def insert(self,payload:BirdCreate):
        species_obj = self.session.get(Species,payload.species_id)    
        if not species_obj:
            raise HTTPException(status_code=404,detail="Species not found")
        item = Bird.model_validate(payload)
        self.session.add(item) 
        self.session.commit()
        self.session.refresh(item)
        return item