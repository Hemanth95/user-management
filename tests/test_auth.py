from fastapi.testclient import TestClient
from src.main import app
from src.models import User
from src.db_utils import get_db_session
from src.security import get_password_hash
import pytest

@pytest.fixture()
def client():
    return TestClient(app)



def test_register_user(client):
    with get_db_session() as db:
        initial_user_count = db.query(User).count()
        response = client.post(
            "/auth/register",
            json={"username": "testuser", "email": "testuser@example.com", "password": "testpassword"},
        )
        assert response.status_code == 200
        assert db.query(User).count() == initial_user_count + 1
        db.query(User).filter(User.username == "testuser").delete()
        db.commit()

def test_login(client):
    with get_db_session() as db:
        db.add(User(username="testuser", email="testuser@example.com", hashed_password=get_password_hash("testpassword")))
        db.commit()
        response = client.post(
            "/auth/login",
            data={"username": "testuser", "password": "testpassword"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        db.query(User).filter(User.username == "testuser").delete()
        db.commit()