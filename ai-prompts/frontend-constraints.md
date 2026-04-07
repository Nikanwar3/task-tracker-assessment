# Frontend AI Prompt Constraints

These constraints were given to the AI assistant when generating frontend code.

## Stack
- React 18 with functional components and hooks only
- Vite as build tool
- Vanilla CSS (no CSS frameworks)
- No state management library — React useState/useEffect only

## File Structure Rules
- All API calls go through `src/api/taskApi.js` only
- All magic strings (statuses, priorities, labels, transitions) live in `src/utils/constants.js`
- Each component has one responsibility — form, list, filter bar
- No inline styles — all styling in `App.css`

## Validation Rules
- Frontend validates before submitting to API
- Title cannot be empty
- Due date cannot be in the past
- Display field-level error messages near each input
- Prevent double submission

## State Handling Rules
- Always show a loading indicator while fetching
- Always show an empty state message when the list is empty
- Always show an error banner when an API call fails
- Errors must be dismissible

## Status Transition Rules
- Buttons to change status are rendered only for valid next transitions
- `ALLOWED_TRANSITIONS` in `constants.js` drives which buttons appear
- Archived tasks show no edit button
- Status change is PATCH to `/tasks/:id/status`; update details is PUT to `/tasks/:id`

## API Contract
- Base URL: `http://localhost:5000`
- Errors from API are surfaced in the error banner with the message from `data.error`
- Marshmallow errors (`data.errors`) are flattened into a single message string

## Style Rules
- Use semantic HTML (form, button, label, etc.)
- All interactive elements must be keyboard accessible
- Responsive layout using CSS grid/flex — no fixed widths
