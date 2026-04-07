from flask import Blueprint, request, jsonify
from marshmallow import ValidationError as MarshmallowValidationError
from schemas.task_schema import task_schema, tasks_schema, task_update_schema, status_update_schema
from services import task_service
from services.task_service import TaskNotFoundError, InvalidTransitionError, ValidationError

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


@tasks_bp.route("", methods=["POST"])
def create_task():
    json_data = request.get_json()
    if not json_data:
        return error_response("Request body must be JSON.", 400)
    try:
        data = task_schema.load(json_data)
    except MarshmallowValidationError as err:
        return jsonify({"errors": err.messages}), 422

    task = task_service.create_task(data)
    return jsonify(task_schema.dump(task)), 201


@tasks_bp.route("", methods=["GET"])
def list_tasks():
    status = request.args.get("status")
    priority = request.args.get("priority")
    try:
        tasks = task_service.get_all_tasks(status=status, priority=priority)
    except ValidationError as e:
        return error_response(str(e), 400)
    return jsonify(tasks_schema.dump(tasks)), 200


@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    try:
        task = task_service.get_task_by_id(task_id)
    except TaskNotFoundError as e:
        return error_response(str(e), 404)
    return jsonify(task_schema.dump(task)), 200


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    json_data = request.get_json()
    if not json_data:
        return error_response("Request body must be JSON.", 400)
    try:
        data = task_update_schema.load(json_data)
        task = task_service.update_task(task_id, data)
    except MarshmallowValidationError as err:
        return jsonify({"errors": err.messages}), 422
    except TaskNotFoundError as e:
        return error_response(str(e), 404)
    except InvalidTransitionError as e:
        return error_response(str(e), 409)
    return jsonify(task_schema.dump(task)), 200


@tasks_bp.route("/<int:task_id>/status", methods=["PATCH"])
def update_status(task_id):
    json_data = request.get_json()
    if not json_data:
        return error_response("Request body must be JSON.", 400)
    try:
        data = status_update_schema.load(json_data)
        task = task_service.update_task_status(task_id, data["status"])
    except MarshmallowValidationError as err:
        return jsonify({"errors": err.messages}), 422
    except TaskNotFoundError as e:
        return error_response(str(e), 404)
    except InvalidTransitionError as e:
        return error_response(str(e), 409)
    return jsonify(task_schema.dump(task)), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        task_service.delete_task(task_id)
    except TaskNotFoundError as e:
        return error_response(str(e), 404)
    return jsonify({"message": "Task deleted."}), 200
