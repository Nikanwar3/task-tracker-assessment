# AI Code Review Checklist

Used after every AI-generated code block before it was accepted into the project.

## Backend Review
- [ ] Does the route call the schema before the service?
- [ ] Does the service raise custom exceptions (not generic ones)?
- [ ] Does the route return the correct HTTP status code for each exception type?
- [ ] Are all valid/invalid values sourced from constants (not hardcoded)?
- [ ] Does the status transition go through `Task.can_transition_to()`?
- [ ] Is the archived-task edit guard present in the update service method?
- [ ] Does the schema strip and validate the title properly?
- [ ] Are `created_at` and `updated_at` never accepted from user input?

## Frontend Review
- [ ] Are all API calls routed through `taskApi.js`?
- [ ] Are status and priority values sourced from `constants.js`?
- [ ] Are loading, empty, and error states all handled?
- [ ] Does form validation run before the API call is made?
- [ ] Are transition buttons gated by `ALLOWED_TRANSITIONS`?
- [ ] Is the error banner dismissible?

## Test Review
- [ ] Does each test have a descriptive name that states what it proves?
- [ ] Is there a test for the happy path and each rejection?
- [ ] Does the test use `TestingConfig` (in-memory DB)?
- [ ] Are there no mocks replacing DB calls?

## What was reviewed manually before acceptance
- All validation logic in `task_schema.py`
- All transition logic in `models/task.py`
- All service-level guards in `task_service.py`
- All error response paths in `task_routes.py`
- Constants match between frontend (`constants.js`) and backend (`models/task.py`)
