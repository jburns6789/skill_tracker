import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import FastAPI
from app.main import app
from app.database import get_db as get_db_async, AsyncSessionLocal  
from app.auth.dependencies import get_current_user
from app.models.models import User

@pytest_asyncio.fixture(scope="function")
async def async_client():
    async def override_get_db():
        async with AsyncSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()

    def override_get_current_user():
        return User(id=1, username="testuser", email="test@example.com")

    app.dependency_overrides[get_db_async] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_skill(async_client):
    response = await async_client.post(
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

@pytest.mark.asyncio
async def test_get_skills(async_client):
    await async_client.post(
        "/skills",
        json={
            "name": "TestingSkill",
            "category_id": 1,
        }
    )
    response = await async_client.get("/skills")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "TestingSkill"
