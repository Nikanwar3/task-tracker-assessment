# AGENTS.md — AI Coding Rules for Task Tracker

## Purpose
This file communicates the project's coding constraints to any AI assistant used during development.
It ensures AI-generated code aligns with the architecture, validation rules, and quality bar set by the developer.

## General Rules
- Do not add features that were not explicitly requested.
- Keep code simple, readable, and modular. No clever one-liners at the expense of clarity.
- Do not modify files unrelated to the current change.
- Add comments only where logic is non-obvious.
- Never skip validation — every endpoint must validate its inputs.

## Backend (Flask)
- All business logic lives in `services/task_service.py`. Routes must stay thin.
- Use `marshmallow` schemas (`schemas/task_schema.py`) to validate request bodies before they touch the service layer.
- Return structured JSON errors with appropriate HTTP status codes:
  - `400` — bad request / invalid filter param
  - `404` — resource not found
  - `409` — invalid business rule (e.g. illegal status transition)
  - `422` — schema validation failure
- Use constants/enums for `status` and `priority` values — never hardcode strings.
- All status transitions must go through `Task.can_transition_to()` in the model.
- Archived tasks must not be edited without a restore step.
- Do not use `app.config` directly inside route files — use the app factory pattern.

## Database
- SQLite is the default; schema managed by SQLAlchemy.
- Do not use raw SQL — use ORM models only.
- `created_at` and `updated_at` must be system-generated; never accept them from user input.

## Frontend (React)
- API calls must go through `src/api/taskApi.js` only — no direct `fetch` calls inside components.
- Status and priority values must reference `src/utils/constants.js` — never hardcode strings.
- Form validation must happen on the frontend **and** the backend independently.
- Empty states, loading states, and error states must always be handled and displayed.
- Allowed status transitions shown in the UI must match `ALLOWED_TRANSITIONS` in `constants.js`.

## Testing
- Every new endpoint behavior must have a corresponding test in `tests/test_tasks.py`.
- Tests must use the in-memory SQLite database via `TestingConfig`.
- Tests are named after what they verify — `test_create_task_empty_title_rejected`, not `test_2`.
- Do not mock the database in tests.

## Submission Standards
- All files reviewed by the developer before acceptance.
- AI-generated code is not accepted without manual verification of validation logic, status transitions, and error paths.
