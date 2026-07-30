# HTTP APIs Assignment (FastAPI) — REST & GraphQL

## Goal of This Assignment

Build a RESTful API server using **FastAPI** that demonstrates:

1. **RESTful endpoints** — GET, POST, PUT, DELETE with proper status codes and response models
2. **Pydantic models** — data validation via `BaseModel` for courses, lecturers, and students
3. **Router organization** — `APIRouter` to split routes by domain (`courses.py`, `lecturers.py`, `students.py`)
4. **JSON persistence** — load/save JSON files as a lightweight store
5. **GraphQL integration** — Strawberry schema with Pydantic types, queries, and mutations

---

## Project Structure

```
fastapi_project/
├── http_apis/main.py          # FastAPI app + GraphQL setup (entry point)
│
├── models/
│   ├── course.py              # Course Pydantic model
│   ├── lecturer.py            # Lecturer Pydantic model
│   └── student.py             # Student Pydantic model
│
├── routers/
│   ├── courses.py             # Courses CRUD routes (GET, POST, PUT, DELETE)
│   ├── lecturers.py           # Lecturers CRUD routes (GET, POST, PUT, DELETE)
│   └── students.py            # Students CRUD routes (GET, POST, PUT, DELETE)
│
├── data/
│   ├── courses.json           # Course data store
│   ├── lecturers.json         # Lecturer data store
│   └── students.json          # Student data store
│
├── HTTP-APIs SourceFiles/     # ⚠️ Duplicate copy — only keep the real source above
```

---

## Endpoints

### REST API (base path: `/mct`)

| Entity    | GET all     | GET by name       | GET by track  | POST create | PUT update | DELETE |
|-----------|-------------|-------------------|---------------|-------------|------------|--------|
| Courses   | ✅          | ✅                | ✅            | ✅          | ✅         | ✅     |
| Lecturers | ✅          | ✅                | ✅            | ✅          | ❌         | ✅     |
| Students  | ✅          | ✅                | ✅            | ✅          | ❌         | ✅     |

**Example routes:**
- `GET /mct/courses` — returns all courses as `Course` objects (via response model)
- `GET /mct/lecturers/name/Jane` — filter lecturers by name
- `POST /mct/students` — create a new student, persists to JSON file
- `PUT /mct/courses/3` — update course at index 3

**Status codes used:**
- `200 OK` for successful GETs and PUTs
- `201 Created` for POST endpoints
- `404 Not Found` when an entity index doesn't exist (PUT/DELETE)

### GraphQL API (`/graphql`)

| Operation    | Field       | Description                        |
|-------------|-------------|------------------------------------|
| Query       | `lecturers` | Return all lecturers               |
| Query       | `courses`   | Return all courses                 |
| Query       | `students`  | Return all students                |
| Mutation    | `add_lecturer(name, language, track, programmingLanguage, favouriteCourse)` | Create lecturer |
| Mutation    | `add_student(...)` | Create student               |
| Mutation    | `add_course(title, content, semester, pillar, tags)` | Create course |

### API Testing (Postman)

A Postman workspace is provided in `HTTP-APIs SourceFiles/postman/` to test all endpoints:

- **Globals** — workspace-level variables (base URL, auth tokens)
- **Collections** — grouped by entity (`Courses`, `Lecturers`, `Students`) with sample requests
- **Environments** — environment configs for different deployment targets
- **Flows** — multi-step request chains (e.g., create → read → update → delete in sequence)

### Swagger & GraphQL URLs

| Resource | URL |
|----------|-----|
| REST API docs (Swagger UI) | `http://localhost:8000/docs` |
| Alternative OpenAPI JSON | `http://localhost:8000/openapi.json` |
| ReDoc (alternative UI) | `http://localhost:8000/redoc` |
| GraphQL Playground | `http://localhost:8000/graphql` |

---

## Key Concepts Demonstrated

### 1. Pydantic Models as Request/Response Contracts

Each model extends `BaseModel` — FastAPI automatically:
- **Validates** incoming request bodies against the schema
- **Serializes** response models to JSON via `response_model=`
- Generates Swagger docs with field descriptions and types

```python
class Course(BaseModel):
    title: str
    content: str
    semester: int
    pillar: str
    tags: List[str]
```

### 2. Router-Based Organization

Routes are split across modules using `APIRouter` — each entity (courses, lecturers, students) has its own file. The main app collects them via `app.include_router(...)`. This keeps code modular and scaleable.

### 3. JSON Persistence Layer

Data lives in `.json` files loaded at startup. Each router exposes a `save_X()` function that writes back after mutations (POST/PUT/DELETE). Simple but functional for small datasets.

### 4. Strawberry GraphQL Schema

Pydantic models are converted to GraphQL types using `@strawberry.experimental.pydantic.type(model=..., all_fields=True)`. Queries and mutations use the `@strawberry.field` / `@strawberry.mutation` decorators. The schema is mounted via `GraphQLRouter(schema, path="/graphql")`.

### 5. Lambda + Filter Pattern

Filtering uses Python's built-in `filter()` with lambda expressions:
```python
filtered = filter(
    lambda course: course["tracks"] is None or track in course["tracks"],
    courses
)
return list(map(lambda c: Course(**c), filtered))
```

---

## How to Run

```bash
# Install dependencies
pip install fastapi uvicorn strawberry-graphql[fastapi] python-multipart json

# Start the server (on port 8000 by default)
uvicorn http_apis.main:app --reload

# Open Swagger docs at http://localhost:8000/docs
# Open GraphQL Playground at http://localhost:8000/graphql
```

---

## What's Still Missing (Optional Extensions)

| Feature | Effort | Notes |
|---------|--------|-------|
| **Path validation on IDs** | Small | Ensure `course_id`, `lecturer_id`, `student_id` are integers in route signatures |
| **Error handling for invalid JSON** | Small | Wrap file reads/loads in try-except |
| **Authentication middleware** | Medium | API key or JWT-based auth for write endpoints |
| **Database backend (SQLAlchemy)** | Large | Replace JSON files with a proper relational DB |

---

## How to Present This During Your Sketch Session

1. Walk through the project structure — point out how routers are split by domain and collected in `main.py`
2. Explain why Pydantic models are used as both request bodies AND response types (validation + serialization)
3. Demo a GET endpoint, then show the Swagger UI auto-generated docs
4. Point out where the router pattern is used vs. inline route definitions
5. Show the GraphQL playground — run a query to fetch lecturers, then a mutation to add one
6. Open Postman workspace and demonstrate a few requests (GET all courses, POST new student) as an alternative testing method
7. Explain the JSON persistence flow: load at startup → mutate in memory → save back to file
