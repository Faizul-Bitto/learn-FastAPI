from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
from ..models import Todos, Users

from ..database import Base
from ..main import app
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@localhost/todos_app_test"

engine = create_engine(SQLALCHEMY_DATABASE_URI)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# -----------------------------
# Dependency Overrides
# -----------------------------


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"user_id": 1, "user_name": "john", "user_role": "admin"}


client = TestClient(app)


# -----------------------------
# Fixture
# -----------------------------
@pytest.fixture
def test_user():
    db = TestingSessionLocal()

    # Clean database
    db.execute(text("DELETE FROM todos"))
    db.execute(text("ALTER TABLE todos AUTO_INCREMENT = 1"))

    db.execute(text("DELETE FROM users"))
    db.execute(text("ALTER TABLE users AUTO_INCREMENT = 1"))

    db.commit()

    user = Users(
        email="john@test.com",
        user_name="john",
        first_name="John",
        last_name="Doe",
        hashed_password=bcrypt_context.hash("password"),
        role="admin",
        is_active=True,
        phone_number="01700000000",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    yield user

    db.execute(text("DELETE FROM todos"))
    db.execute(text("DELETE FROM users"))
    db.commit()
    db.close()


@pytest.fixture
def test_todo(test_user):
    db = TestingSessionLocal()

    todo = Todos(
        title="Test",
        description="Test",
        priority=5,
        complete=False,
        owner_id=test_user.id
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)

    yield todo

    db.close()