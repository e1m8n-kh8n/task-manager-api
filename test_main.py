
import pytest
from fastapi.testclient import TestClient

import database
from main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Give each test its own temporary database
    test_db = tmp_path / "test_tasks.db"
    monkeypatch.setattr(database, "DATABASE_NAME", str(test_db))

    # Start the app and initialize its test database
    with TestClient(app) as test_client:
        yield test_client


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "My Task Manager API is running!"
    }


def test_create_and_get_task(client):
    response = client.post("/tasks", json={
        "title": "Study Python",
        "completed": False
    })

    assert response.status_code == 201
    assert response.json()["title"] == "Study Python"

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Study Python"


def test_update_task(client):
    created = client.post("/tasks", json={
        "title": "Finish resume",
        "completed": False
    })

    task_id = created.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={
        "title": "Finish resume",
        "completed": True
    })

    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_task(client):
    created = client.post("/tasks", json={
        "title": "Delete this task",
        "completed": False
    })

    task_id = created.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200

    remaining = client.get("/tasks").json()
    assert remaining == []


def test_missing_task(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
