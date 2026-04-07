from datetime import datetime, timezone
from models.task import Task, VALID_PRIORITIES, VALID_STATUSES
from extensions import db


class TaskNotFoundError(Exception):
    pass


class InvalidTransitionError(Exception):
    pass


class ValidationError(Exception):
    pass


def get_all_tasks(status=None, priority=None):
    query = Task.query
    if status:
        if status not in VALID_STATUSES:
            raise ValidationError(f"Invalid status filter: {status}")
        query = query.filter_by(status=status)
    if priority:
        if priority not in VALID_PRIORITIES:
            raise ValidationError(f"Invalid priority filter: {priority}")
        query = query.filter_by(priority=priority)
    return query.order_by(Task.created_at.desc()).all()


def get_task_by_id(task_id):
    task = Task.query.get(task_id)
    if not task:
        raise TaskNotFoundError(f"Task {task_id} not found.")
    return task


def create_task(data: dict) -> Task:
    task = Task(
        title=data["title"],
        description=data.get("description"),
        priority=data.get("priority", "medium"),
        status=data.get("status", "todo"),
        due_date=data.get("due_date"),
    )
    db.session.add(task)
    db.session.commit()
    return task


def update_task(task_id: int, data: dict) -> Task:
    task = get_task_by_id(task_id)
    if task.status == "archived":
        raise InvalidTransitionError("Archived tasks cannot be edited. Restore the task first.")

    for field in ("title", "description", "priority", "due_date"):
        if field in data:
            setattr(task, field, data[field])

    task.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return task


def update_task_status(task_id: int, new_status: str) -> Task:
    task = get_task_by_id(task_id)
    if not task.can_transition_to(new_status):
        raise InvalidTransitionError(
            f"Cannot move task from '{task.status}' to '{new_status}'."
        )
    task.status = new_status
    task.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return task


def delete_task(task_id: int):
    task = get_task_by_id(task_id)
    db.session.delete(task)
    db.session.commit()
