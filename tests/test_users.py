import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models import User, Role, UserRole
from src.db_utils import get_db_session
from src.security import get_password_hash
import pytest

@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def test_token(client):
    response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "admin123!"},
    )
    return response.json()["access_token"]

def test_get_users(client, test_token):
    response = client.get("/users/",headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200


def test_get_profile(client):
    # Create a test user
    db = get_db_session()
    test_user = User(username="testuser-p2", hashed_password = get_password_hash("testpassword"))
    db.add(test_user)
    db.commit()

    token = client.post(
        "/auth/login",
        data={"username": "testuser-p2", "password": "testpassword"},
    )
    test_token = token.json()["access_token"]
    response = client.get("/users/profile", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser-p2"

    # Delete the test user
    db.delete(test_user)
    db.commit()

def test_assign_role_to_user(client, test_token):
    db = get_db_session()
    test_user = User(username="testuser", is_admin=True, hashed_password = get_password_hash("testpassword"))
    test_role = Role(name="testrole")
    db.add(test_user)
    db.add(test_role)
    db.commit()

    admin = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword"},
    )
    admin_token = admin.json()["access_token"]
    response = client.post(f"/users/{test_user.id}/roles", json={"name": "testrole"},headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Role assigned to user successfully."

    # Delete the test user and the test role
    user_role = db.query(UserRole).filter(UserRole.user_id == test_user.id, UserRole.role_id == test_role.id).first()
    db.delete(user_role)
    db.delete(test_user)
    db.delete(test_role)
    db.commit()