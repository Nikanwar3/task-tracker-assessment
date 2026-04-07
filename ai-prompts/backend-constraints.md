# Backend AI Prompt Constraints

These constraints were given to the AI assistant when generating backend code.

## Stack
- Python 3.11+
- Flask 3.x with app factory pattern
- SQLAlchemy (via flask-sqlalchemy)
- Marshmallow (via flask-marshmallow) for validation
- SQLite for development; schema defined via ORM models
- pytest for testing

## Architecture Rules
- `app.py` — only app factory and blueprint registration
- `config.py` — config classes only; no business logic
- `extensions.py` — db and ma singletons only
- `models/task.py` — SQLAlchemy model + transition logic only
- `schemas/task_schema.py` — marshmallow validation only
- `services/task_service.py` — all business logic; raises custom exceptions
- `routes/task_routes.py` — calls schema, calls service, returns JSON; no logic

## Validation Requirements
- Title: required, non-empty after stripping whitespace, max 255 chars
- Priority: must be one of `low | medium | high`
- Status: must be one of `todo | in_progress | done | archived`
- Due date: optional; if provided, must not be in the past
- description: optional text

## Status Transition Rules (enforced in model)
```
todo        → in_progress | archived
in_progress → todo | done | archived
done        → archived
archived    → todo  (explicit restore)
```
- Archived tasks cannot be edited (update endpoint must reject with 409)

## Error Format
All errors return JSON:
```json
{ "error": "Human-readable message" }
```
Marshmallow validation errors return:
```json
{ "errors": { "field": ["message"] } }
```

## Testing Rules
- Use `TestingConfig` with `SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"`
- Each test gets a fresh database via pytest fixture
- No mocks — real ORM calls against in-memory SQLite
- Test both happy path and every rejection path
