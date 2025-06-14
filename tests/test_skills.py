import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth.dependencies import get_current_user
from app.models.models import User
from app.database import AsyncSessionLocal, get_db


@pytest.fixture(scope="function")
def client():
    """Fixture providing a TestClient with mocked dependencies."""
    def override_get_db():
        db = AsyncSessionLocal()
        try:
            yield db
        finally:
            db.close()

    def override_get_current_user():
        return User(id=1, username="testuser", email="test@example.com")

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_create_skill(client):
    """Test skill creation endpoint."""
    response = client.post(
        "/skills",
        json={
            "name": "TestingSkill",
            "category_id": 1,
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "TestingSkill"
    assert data["category_id"] == 1
    assert "id" in data
    assert data["user_id"] == 1

def test_get_skills(client):
    """Test skill listing endpoint."""
    # First, create a skill so there is something to list
    client.post(
        "/skills",
        json={
            "name": "TestingSkill",
            "category_id": 1,
        }
    )
    response = client.get("/skills")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "TestingSkill"
