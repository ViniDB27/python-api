import pytest
import requests

# CRUD
BASE_URL = "http://127.0.0.1:5000"
tasks = []

def test_create_task():
    new_task = {
        "title": "Test Task", 
        "description": "This is a test task."
    }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task)
    data = response.json()
    tasks.append(data["id"])
    assert response.status_code == 200
    assert "message" in data
    assert "id" in data


def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    data = response.json()
    assert response.status_code == 200
    assert "tasks" in data
    assert "total" in data
    assert isinstance(data['tasks'], list)

def test_get_task():
    task_id = tasks[0]
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    data = response.json()
    assert response.status_code == 200
    assert "id" in data
    assert data["id"] == task_id

def test_update_task():
    task_id = tasks[0]
    updated_task = {
        "title": "Updated Test Task",
        "description": "This is an updated test task.",
        "completed": True
    }
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=updated_task)
    data = response.json()
    assert response.status_code == 200
    assert "message" in data

def test_delete_task():
    task_id = tasks[0]
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    data = response.json()
    assert response.status_code == 200
    assert "message" in data
    tasks.remove(task_id)