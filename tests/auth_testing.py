import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth.dependencies import get_current_user
from app.models.models import User
from app.database import SessionLocal
from app.database import get_db as get_db_async  # Use your real async get_db import

@pytest.fixture(scope="function")
def client():
    """Fixture providing a TestClient with mocked dependencies."""
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def override_get_current_user():
        return User(id=1, username="testuser", email="test@example.com")

    app.dependency_overrides[get_db_async] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_register_user(client):
    """Test user registration endpoint."""
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "TestPass123!"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}

def test_register_user_duplicate_email(client):
    # First registration
    client.post(
        "/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "TestPass123!"}
    )
    # Second registration with same email
    response = client.post(
        "/auth/register",
        json={"username": "testuser2", "email": "test@example.com", "password": "TestPass123!"}
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_login_user(client):
    # Register first
    client.post(
        "/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "TestPass123!"}
    )
    # Then login
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "TestPass123!"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
