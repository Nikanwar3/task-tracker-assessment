# Task Tracker — Associate Software Engineer Assessment

A full-stack Task Tracker built with **Flask**, **React**, and **SQLite**.
Demonstrates clean layered architecture, enforced business rules, input validation, and meaningful test coverage.

---

## Tech Stack

| Layer    | Technology                                      |
|----------|-------------------------------------------------|
| Frontend | React 18, Vite, Vanilla CSS                    |
| Backend  | Flask 3, SQLAlchemy, Marshmallow, Flask-CORS   |
| Database | SQLite (development) — PostgreSQL-ready via env var |
| Testing  | pytest with in-memory SQLite                    |

---

## Architecture Summary

```
Browser (React)
     │  HTTP JSON
     ▼
Flask Routes  ← validates schema
     │
Flask Service ← enforces business rules
     │
SQLAlchemy ORM
     │
SQLite (tasks.db)
```

- **Routes** are thin: parse JSON, call schema, call service, return JSON.
- **Service layer** owns all business logic and raises typed exceptions.
- **Model** owns transition rules (`can_transition_to`).
- **Schemas** (Marshmallow) validate every incoming payload before the service layer sees it.
- **Frontend** mirrors all constants and transition rules from `utils/constants.js`.

---

## Folder Structure

```
task-tracker-assessment/
├── backend/
│   ├── app.py                  # Flask app factory
│   ├── config.py               # Config classes (default + testing)
│   ├── extensions.py           # db and ma singletons
│   ├── models/task.py          # SQLAlchemy model + transition logic
│   ├── schemas/task_schema.py  # Marshmallow validation schemas
│   ├── services/task_service.py# All business rules
│   ├── routes/task_routes.py   # Blueprint with API endpoints
│   ├── tests/test_tasks.py     # pytest test suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/taskApi.js      # All fetch calls
│   │   ├── components/
│   │   │   ├── FilterBar.jsx
│   │   │   ├── TaskForm.jsx
│   │   │   └── TaskList.jsx
│   │   ├── pages/Dashboard.jsx
│   │   ├── utils/constants.js  # Status/priority enums + transitions
│   │   ├── App.jsx
│   │   └── App.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── ai-prompts/
│   ├── backend-constraints.md
│   ├── frontend-constraints.md
│   └── ai-review-checklist.md
├── AGENTS.md
└── README.md
```

---

## How to Run — Backend

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

API runs at **http://localhost:5000**

---

## How to Run — Frontend

```bash
cd frontend

npm install
npm run dev
```

UI runs at **http://localhost:3000**

---

## Database Setup

SQLite is used by default. The database file (`backend/tasks.db`) is created automatically on first run via `db.create_all()`.

To switch to PostgreSQL, set the environment variable before starting the server:

```bash
export DATABASE_URL="postgresql://user:password@localhost/tasktracker"
python app.py
```

---

## API Endpoints

| Method | Endpoint               | Purpose              |
|--------|------------------------|----------------------|
| POST   | `/tasks`               | Create a task        |
| GET    | `/tasks`               | List tasks (filterable by `?status=` and `?priority=`) |
| GET    | `/tasks/<id>`          | Get single task      |
| PUT    | `/tasks/<id>`          | Update task details  |
| PATCH  | `/tasks/<id>/status`   | Update status only   |
| DELETE | `/tasks/<id>`          | Delete a task        |
| GET    | `/health`              | Health check         |

---

## Business Rules Enforced

- Title is required and cannot be blank (stripped whitespace counts as empty)
- Priority must be one of: `low | medium | high`
- Status must be one of: `todo | in_progress | done | archived`
- Due date, if provided, must not be in the past
- **Status transitions** follow a strict state machine:
  ```
  todo        → in_progress, archived
  in_progress → todo, done, archived
  done        → archived
  archived    → todo  (explicit restore only)
  ```
- **Archived tasks cannot be edited** — a 409 is returned; restore first
- `created_at` and `updated_at` are system-managed; not accepted from user input

---

## Testing Instructions

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

Expected output: **15 passing tests**

### What the tests cover

| Category            | Tests                                               |
|---------------------|-----------------------------------------------------|
| Create              | Success, empty title, missing title, invalid priority, invalid status |
| Read                | Get by ID, 404 on unknown ID, list all, filter by status, invalid filter |
| Update              | Success, reject edit of archived task               |
| Status transitions  | Valid transition, invalid transition, restore archived |
| Delete              | Success, 404 on unknown IDs                         |

---

## Key Technical Decisions

**Why SQLite?**
Fast to set up for a 48-hour assessment. The schema is portable — switching to PostgreSQL requires only a `DATABASE_URL` env var change. Noted in the README.

**Why no authentication?**
Auth was out of scope for this assessment. Adding it would mean a `users` table and JWT middleware — doable, but would not improve the score compared to a complete, validated core.

**Why a service layer?**
Routes that contain business logic become hard to test and reuse. The service layer holds all rules (transition guards, archived-edit guard) and raises typed exceptions. Routes stay to ~10 lines each.

**Why Marshmallow over manual dict access?**
Marshmallow makes the validation contract explicit and self-documenting. `@validates` decorators run inline, and the schema `load()` call is one line in the route.

**Why status transitions in the model, not the service?**
`can_transition_to()` is a property of the entity itself — it describes what a task knows about itself. Keeping it in the model means it cannot be bypassed by any service method that touches status.

---

## AI Usage Summary

AI was used as a coding assistant under explicit constraints (see `AGENTS.md` and `ai-prompts/`).

| What AI helped generate | What was manually reviewed / changed |
|------------------------|--------------------------------------|
| Initial folder structure scaffold | Verified structure matched assessment spec |
| Marshmallow schema fields | Validated `@validates` logic for title/due_date |
| Service layer exception types | Confirmed all exceptions are caught in routes with correct HTTP codes |
| Status transition map | Cross-checked against assessment rules and frontend constants |
| Test file structure | Added missing transition tests; renamed tests for clarity |
| CSS layout | Adjusted spacing, badge colors, and modal behavior |

Every AI-generated file was reviewed line-by-line using the checklist in `ai-prompts/ai-review-checklist.md` before being accepted.

---

## Known Limitations and Future Improvements

- **No authentication** — all tasks are global; a `user_id` FK and JWT auth would scope tasks per user
- **No pagination** — a large task list would need cursor-based pagination on `/tasks`
- **No soft-delete** — delete is permanent; an `is_deleted` flag would allow recovery
- **SQLite not suitable for production** — concurrent writes will serialize; move to PostgreSQL
- **No frontend tests** — Vitest + React Testing Library would cover form validation edge cases
- **No CI/CD** — a GitHub Actions workflow would run `pytest` on every push
