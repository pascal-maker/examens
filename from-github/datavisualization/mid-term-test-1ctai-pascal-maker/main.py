from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_db_and_tables, engine
from routers.robots import router as robots_router
from routers.functionalities import router as functionalities_router


app = FastAPI(title="Robot Management API")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    _seed_data()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(robots_router, prefix="/api")
app.include_router(functionalities_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Robot Management API — visit /docs"}



def _seed_data():
    from sqlmodel import Session, select
    from models.functionality import Functionality
    from models.robot import Robot

    with Session(engine) as session:
        if session.exec(select(Functionality)).first():
            return  

        funcs = [
            Functionality(name="Dance",    description="Perform a short dance routine."),
            Functionality(name="Talk",     description="Speak a short scripted message."),
            Functionality(name="Lift",     description="Move and lift light objects."),
            Functionality(name="Scan",     description="Scan nearby objects or markers."),
        ]
        for f in funcs:
            session.add(f)
        session.commit()
        for f in funcs:
            session.refresh(f)

        robots = [
            Robot(name="Astra", location="Lab 1",        ip_address="10.0.1.21", current_functionality_id=funcs[0].id),
            Robot(name="Bolt",  location="Hallway Dock", ip_address="10.0.1.22", current_functionality_id=funcs[1].id),
            Robot(name="Cleo",  location="Workshop A",   ip_address="10.0.1.23", current_functionality_id=funcs[2].id),
            Robot(name="Drift", location="Charging Bay", ip_address="10.0.1.24", current_functionality_id=funcs[3].id),
            Robot(name="Echo",  location="Storage Room", ip_address="10.0.1.25", current_functionality_id=funcs[0].id),
        ]
        for r in robots:
            session.add(r)
        session.commit()
