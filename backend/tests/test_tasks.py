import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import create_app
from config import TestingConfig
from extensions import db


@pytest.fixture
def client():
    app = create_app(TestingConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


# ── helpers ────────────────────────────────────────────────────────────────

def create_task(client, payload=None):
    if payload is None:
        payload = {"title": "Test Task", "priority": "medium"}
    return client.post("/tasks", json=payload)


# ── CREATE ──────────────────────────────────────────────────────────────────

def test_create_task_success(client):
    res = create_task(client, {"title": "Buy groceries", "priority": "low"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Buy groceries"
    assert data["status"] == "todo"
    assert data["priority"] == "low"


def test_create_task_empty_title_rejected(client):
    res = create_task(client, {"title": "   ", "priority": "medium"})
    assert res.status_code == 422
    errors = res.get_json()["errors"]
    assert "title" in errors


def test_create_task_missing_title_rejected(client):
    res = create_task(client, {"priority": "high"})
    assert res.status_code == 422


def test_create_task_invalid_priority_rejected(client):
    res = create_task(client, {"title": "Valid title", "priority": "urgent"})
    assert res.status_code == 422


def test_create_task_invalid_status_rejected(client):
    res = create_task(client, {"title": "Valid title", "status": "done_forever"})
    assert res.status_code == 422


# ── READ ────────────────────────────────────────────────────────────────────

def test_get_task_success(client):
    created = create_task(client).get_json()
    res = client.get(f"/tasks/{created['id']}")
    assert res.status_code == 200
    assert res.get_json()["id"] == created["id"]


def test_get_task_not_found(client):
    res = client.get("/tasks/9999")
    assert res.status_code == 404


def test_list_tasks_returns_all(client):
    create_task(client, {"title": "Task A"})
    create_task(client, {"title": "Task B"})
    res = client.get("/tasks")
    assert res.status_code == 200
    assert len(res.get_json()) == 2


def test_list_tasks_filter_by_status(client):
    create_task(client, {"title": "Task A", "status": "todo"})
    create_task(client, {"title": "Task B", "status": "todo"})
    # archive Task B via status endpoint
    task_b_id = client.get("/tasks").get_json()[0]["id"]
    client.patch(f"/tasks/{task_b_id}/status", json={"status": "in_progress"})

    res = client.get("/tasks?status=todo")
    assert res.status_code == 200
    for t in res.get_json():
        assert t["status"] == "todo"


def test_list_tasks_invalid_status_filter(client):
    res = client.get("/tasks?status=flying")
    assert res.status_code == 400


# ── UPDATE ──────────────────────────────────────────────────────────────────

def test_update_task_success(client):
    task = create_task(client, {"title": "Original"}).get_json()
    res = client.put(f"/tasks/{task['id']}", json={"title": "Updated"})
    assert res.status_code == 200
    assert res.get_json()["title"] == "Updated"


def test_update_archived_task_rejected(client):
    task = create_task(client, {"title": "Will be archived"}).get_json()
    # todo -> in_progress -> done -> archived
    client.patch(f"/tasks/{task['id']}/status", json={"status": "in_progress"})
    client.patch(f"/tasks/{task['id']}/status", json={"status": "done"})
    client.patch(f"/tasks/{task['id']}/status", json={"status": "archived"})
    res = client.put(f"/tasks/{task['id']}", json={"title": "Sneaky edit"})
    assert res.status_code == 409


# ── STATUS TRANSITIONS ──────────────────────────────────────────────────────

def test_valid_status_transition(client):
    task = create_task(client).get_json()
    res = client.patch(f"/tasks/{task['id']}/status", json={"status": "in_progress"})
    assert res.status_code == 200
    assert res.get_json()["status"] == "in_progress"


def test_invalid_status_transition_rejected(client):
    task = create_task(client).get_json()  # status = todo
    res = client.patch(f"/tasks/{task['id']}/status", json={"status": "done"})
    assert res.status_code == 409


def test_restore_archived_task(client):
    task = create_task(client).get_json()
    client.patch(f"/tasks/{task['id']}/status", json={"status": "archived"})
    res = client.patch(f"/tasks/{task['id']}/status", json={"status": "todo"})
    assert res.status_code == 200
    assert res.get_json()["status"] == "todo"


# ── DELETE ──────────────────────────────────────────────────────────────────

def test_delete_task_success(client):
    task = create_task(client).get_json()
    res = client.delete(f"/tasks/{task['id']}")
    assert res.status_code == 200
    assert client.get(f"/tasks/{task['id']}").status_code == 404


def test_delete_task_not_found(client):
    res = client.delete("/tasks/9999")
    assert res.status_code == 404
