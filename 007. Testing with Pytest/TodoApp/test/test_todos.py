from .utils import *
from starlette import status

from ..models import Todos
from ..routers.todos import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


# -----------------------------
# READ ALL
# -----------------------------


def test_read_all_authenticated(test_todo):

    response = client.get("/todos")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == [
        {
            "id": test_todo.id,
            "title": "Test",
            "description": "Test",
            "priority": 5,
            "complete": False,
            "owner_id": 1,
        }
    ]


# -----------------------------
# READ ONE
# -----------------------------


def test_read_one_authenticated(test_todo):

    response = client.get(f"/todos/{test_todo.id}")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        "id": test_todo.id,
        "title": "Test",
        "description": "Test",
        "priority": 5,
        "complete": False,
        "owner_id": 1,
    }


def test_read_one_authenticated_not_found(test_todo):

    response = client.get("/todos/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert response.json() == {"detail": "Not Found"}


# -----------------------------
# CREATE
# -----------------------------


def test_create_todo(test_todo):

    request_data = {
        "title": "New Test",
        "description": "New Test",
        "priority": 5,
        "complete": False,
    }

    response = client.post("/todos/create", json=request_data)

    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()

    todo = db.query(Todos).filter(Todos.id == 2).first()

    assert todo is not None
    assert todo.title == request_data["title"]
    assert todo.description == request_data["description"]
    assert todo.priority == request_data["priority"]
    assert todo.complete == request_data["complete"]

    db.close()


# -----------------------------
# UPDATE
# -----------------------------


def test_update_todo(test_todo):

    request_data = {
        "title": "Changed Test",
        "description": "Changed Description",
        "priority": 3,
        "complete": True,
    }

    response = client.put(f"/todos/update/{test_todo.id}", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()

    todo = db.query(Todos).filter(Todos.id == test_todo.id).first()

    assert todo.title == request_data["title"]
    assert todo.description == request_data["description"]
    assert todo.priority == request_data["priority"]
    assert todo.complete == request_data["complete"]

    db.close()


def test_update_todo_not_found(test_todo):

    request_data = {
        "title": "Changed Test",
        "description": "Changed Description",
        "priority": 3,
        "complete": True,
    }

    response = client.put("/todos/update/999", json=request_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert response.json() == {"detail": "Not Found"}


# -----------------------------
# DELETE
# -----------------------------
def test_delete_todo(test_todo):
    response = client.delete("/todos/delete/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()

    todo = db.query(Todos).filter(Todos.id == 1).first()

    assert todo is None

    db.close()


def test_delete_todo_not_found(test_todo):
    response = client.delete("/todos/delete/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
