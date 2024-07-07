from fastapi.testclient import TestClient
from src.main import app
from src.models import Role, Permission
from src.db_utils import get_db_session
import pytest

@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def admin_token(client):
    response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "admin123!"},
    )
    return response.json()["access_token"]





def test_create_role(client, admin_token):
    with get_db_session() as db:
        initial_role_count = db.query(Role).count()
        response = client.post(
            "/roles/",
            json={"name": "testrole"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert db.query(Role).count() == initial_role_count + 1
        db.query(Role).filter(Role.name == "testrole").delete()
        db.commit()

def test_add_permission_to_role(client, admin_token):
    with get_db_session() as db:
        db.add(Role(name="testrole"))
        db.commit()
        role = db.query(Role).filter(Role.name == "testrole").first()
        response = client.post(
            f"/roles/{role.id}/permissions",
            json={"name": "testpermission"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert any(permission.name == "testpermission" for permission in role.permissions)
        permissions = db.query(Permission).filter(Permission.name == "testpermission").first()
        for role in permissions.roles:
            role.permissions.remove(permissions)
        db.commit()
        db.query(Role).filter(Role.name == "testrole").delete()
        db.commit()