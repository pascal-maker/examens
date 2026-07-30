# Lab 05 — Birds API (FastAPI + PostgreSQL)

## Goal of This Assignment

Build a relational RESTful API using **FastAPI** and **SQLModel**, backed by **PostgreSQL** via Docker Compose. The project demonstrates:

1. **SQLModel models with relationships** — Species → Birds → Birdspotting
2. **Repository pattern** — `SpeciesRepository`, `BirdRepository`, `BirdSpottingRepository` wrapping SQLModel sessions
3. **Router organization** — routes split by domain (`species.py`, `birds.py`, `birdspotting.py`)
4. **Dependency injection via FastAPI Depends** — shared database session injected into every route handler
5. **Docker Compose infrastructure** — PostgreSQL 18 + Adminer UI for local development

---

## Project Structure

```
lab05_birds/
├── main.py                    # FastAPI app + startup DB migration (entry point)
│
├── models/
│   ├── species.py             # Species model (name, scientific_name, family, conservation_status, wingspan_cm)
│   ├── birds.py               # Bird model (nickname, ring_code, age, species_id → FK to Species)
│   └── birdspotting.py        # BirdSpotting model (spotted_at, location, observer_name, notes, bird_id → FK to Birds)
│
├── repositories/
│   ├── species.py             # SpeciesRepository — get_all(), insert()
│   ├── birds.py               # BirdRepository — get_all(), get_one(), insert()
│   └── birdspotting.py        # BirdSpottingRepository — get_all(), get_one(), insert()
│
├── routers/
│   ├── species.py             # Species CRUD routes (GET /, POST /)
│   ├── birds.py               # Birds CRUD routes (GET /, GET /{id}, POST /)
│   └── birdspotting.py        # Birdspotting CRUD routes (GET /, GET /{id}, POST /)
│
├── database.py                # get_session() dependency + create_db_and_tables()
├── compose.db.yaml            # Docker Compose: postgres:18-alpine + adminer
└── .env                       # Database credentials (DB_HOST, DB_USER, etc.)
```

---

## Data Model

### Species → Birds → Birdspotting

| Table | Fields | Relationships |
|-------|--------|---------------|
| **Species** | `id`, `name`, `scientific_name`, `family`, `conservation_status`, `wingspan_cm` (Decimal) | ← parent of Birds |
| **Birds** | `id`, `nickname`, `ring_code`, `age` (≥0), `species_id` | → belongs to Species, ← parent of Birdspotting |
| **BirdSpotting** | `id`, `spotted_at`, `location`, `observer_name`, `notes`, `bird_id` | → belongs to Birds |

**Foreign key constraints:**
- `birds.species_id → species.id` (RESTRICT on delete)
- `birdspotting.bird_id → birds.id` (CASCADE on delete — spotings deleted when bird is removed)

---

## Endpoints

### Species (`/species`)

| Method | Path | Description | Status Code |
|--------|------|-------------|-------------|
| GET | `/species/` | Return all species | 200 OK |
| POST | `/species/` | Create a new species | 201 Created |

### Birds (`/birds`)

| Method | Path | Description | Status Code |
|--------|------|-------------|-------------|
| GET | `/birds/` | Return all birds (with joined Species) | 200 OK |
| GET | `/birds/{bird_id}` | Get a single bird by ID | 200 OK / 404 Not Found |
| POST | `/birds/` | Create a new bird (requires species_id) | 201 Created |

### Birdspotting (`/birdspotting`)

| Method | Path | Description | Status Code |
|--------|------|-------------|-------------|
| GET | `/birdspotting/` | Return all spotings (with joined Bird) | 200 OK |
| GET | `/birdspotting/{id}` | Get a single sighting by ID | 200 OK / 404 Not Found |
| POST | `/birdspotting/` | Create a new bird spotting (requires bird_id) | 201 Created |

**Example JSON payloads:**

```json
// POST /species/
{
  "name": "African Penguin",
  "scientific_name": "Spheniscus demersus",
  "family": "Spheniscidae",
  "conservation_status": "Endangered",
  "wingspan_cm": 80.50
}

// POST /birds/
{
  "nickname": "Pinky",
  "ring_code": "AP-2024-001",
  "age": 3,
  "species_id": 1
}

// POST /birdspotting/
{
  "location": "Boulders Beach, Simon's Town",
  "observer_name": "Dr. Jane",
  "notes": "Seen with two chicks near the colony entrance",
  "bird_id": 1
}
```

---

## API Testing URLs

| Resource | URL |
|----------|-----|
| REST API docs (Swagger UI) | `http://localhost:8000/docs` |
| Alternative OpenAPI JSON | `http://localhost:8000/openapi.json` |
| ReDoc (alternative UI) | `http://localhost:8000/redoc` |

---

## Key Concepts Demonstrated

### 1. SQLModel with Relationships

SQLModel combines **Pydantic** models with **SQLAlchemy** — each model extends `SQLModel`, and the `table=True` parameter maps it to a database table. Relationships are defined using `Relationship()`:

```python
class Bird(BirdBase, table=True):
    species_id: int = Field(foreign_key="species.id", ondelete="RESTRICT")
    species: Optional[Species] = Relationship()
```

### 2. Repository Pattern

Each domain has a repository class that encapsulates database operations — `get_all()`, `get_one()`, `insert()`. This keeps the router thin and makes testing easier:

```python
class SpeciesRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        statement = select(Species)
        return self.session.exec(statement).all()
```

### 3. Dependency Injection with `Depends`

Database sessions are provided via FastAPI's dependency injection system. Every route handler declares its repository as an annotated parameter:

```python
def get_species_repository(session: Annotated[Session, Depends(get_session)]) -> SpeciesRepository:
    return SpeciesRepository(session)

@router.get("/", response_model=List[Species])
async def get_all_species(
    repo: Annotated[SpeciesRepository, Depends(get_species_repository)]
):
    return repo.get_all()
```

### 4. Docker Compose Infrastructure

PostgreSQL and Adminer run via `compose.db.yaml` — the service reads DB credentials from `.env`:

```yaml
services:
  postgres:
    image: postgres:18-alpine
    env_file: [".env"]
    ports: ["5432:5432"]
    volumes: [db:/var/lib/postgresql/data]

  adminer:
    image: adminer
    ports: ["8081:8080"]
```

---

## How to Run

```bash
# Start PostgreSQL + Adminer via Docker Compose
docker compose -f compose.db.yaml up -d

# Install dependencies
pip install fastapi sqlmodel uvicorn pydantic[email] psycopg2-binary

# Start the server (on port 8000 by default)
uvicorn main:app --reload

# Open Swagger docs at http://localhost:8000/docs
```

---

## How to Present This During Your Sketch Session

1. Walk through the project structure — point out how routers are split by domain and collected in `main.py`
2. Explain SQLModel's dual role as both Pydantic models (request validation) and ORM tables (database schema)
3. Show the data model: Species → Birds → Birdspotting with their foreign key relationships
4. Demo a GET endpoint, then show the Swagger UI auto-generated docs
5. Point out where the repository pattern is used vs. inline queries in route handlers
6. Explain how `Depends(get_session)` provides database sessions to every handler automatically
7. Show Adminer at http://localhost:8081 as an alternative way to inspect data
