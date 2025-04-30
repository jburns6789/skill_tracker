import pytest
import pytest_asyncio

from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.api.routes import get_db
from app.auth.dependencies import get_current_user
from app.models.models import User
from app.database import SessionLocal

@pytest.fixture(scope="function")
def client():
    # Setup dependencies
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def mock_get_current_user():
        return User(id=1, username="testuser")

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = mock_get_current_user
    
    yield TestClient(app)
    
    # Teardown
    app.dependency_overrides.clear()
    
@pytest_asyncio.fixture(scope="function")
async def async_client():
    # Setup dependencies
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def mock_get_current_user():
        return User(id=1, username="testuser")

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = mock_get_current_user

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

    # Teardown
    app.dependency_overrides.clear()

# Test database session
@pytest.fixture(scope="function")
def test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()