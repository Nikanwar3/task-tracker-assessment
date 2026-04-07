from marshmallow import Schema, fields, validate, validates, ValidationError, pre_load
from datetime import date

VALID_PRIORITIES = ["low", "medium", "high"]
VALID_STATUSES = ["todo", "in_progress", "done", "archived"]


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(load_default=None)
    priority = fields.Str(load_default="medium", validate=validate.OneOf(VALID_PRIORITIES))
    status = fields.Str(load_default="todo", validate=validate.OneOf(VALID_STATUSES))
    due_date = fields.Date(load_default=None)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates("title")
    def validate_title(self, value):
        if not value or not value.strip():
            raise ValidationError("Title cannot be empty.")

    @validates("due_date")
    def validate_due_date(self, value):
        if value is not None and value < date.today():
            raise ValidationError("Due date cannot be in the past.")

    @pre_load
    def strip_title(self, data, **kwargs):
        if "title" in data and isinstance(data["title"], str):
            data["title"] = data["title"].strip()
        return data


class TaskUpdateSchema(Schema):
    """Partial update — all fields optional."""
    title = fields.Str()
    description = fields.Str(allow_none=True)
    priority = fields.Str(validate=validate.OneOf(VALID_PRIORITIES))
    due_date = fields.Date(allow_none=True)

    @validates("title")
    def validate_title(self, value):
        if value is not None and not value.strip():
            raise ValidationError("Title cannot be empty.")

    @validates("due_date")
    def validate_due_date(self, value):
        if value is not None and value < date.today():
            raise ValidationError("Due date cannot be in the past.")


class StatusUpdateSchema(Schema):
    status = fields.Str(required=True, validate=validate.OneOf(VALID_STATUSES))


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
task_update_schema = TaskUpdateSchema()
status_update_schema = StatusUpdateSchema()
