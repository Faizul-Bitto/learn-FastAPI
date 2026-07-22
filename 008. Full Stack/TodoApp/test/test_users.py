from starlette import status

from .utils import *
from ..routers.users import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["user_name"] == "john"
    assert response.json()["first_name"] == "John"
    assert response.json()["last_name"] == "Doe"
    assert response.json()["email"] == "john@test.com"
    assert response.json()["role"] == "admin"


def test_change_password_success(test_user):
    response = client.put("/user/change_password", json={
        "hashed_password": "test_password",
        "new_password": "new_password"
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/change_password", json={
        "hashed_password": "wrong_password",
        "new_password": "new_password"
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Not Found"
    }


def test_change_phone_number_success(test_user):
    response = client.put("/user/update_phone_number/22222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT