from database import get_session, create_db_and_tables
from models.species import Species, SpeciesCreate
from repositories.species import SpeciesRepository
try:
    create_db_and_tables()
    session = next(get_session())
    repo = SpeciesRepository(session)
    res = repo.insert(SpeciesCreate(name="Testing"))
    print("Success:", res)
except Exception as e:
    import traceback
    traceback.print_exc()
