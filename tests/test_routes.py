import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

from app.api.routes import get_db
from app.auth.dependencies import get_current_user
from app.models.models import User
from app.database import SessionLocal

#dependencies
#from fastapi import Depends
#from sqlalchemy.orm import Session


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

@pytest.mark.asyncio
async def test_root():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "SkillTree API is working!"}

@pytest.mark.asyncio
async def test_whoami():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/whoami")
        assert response.status_code == 200
        assert response.json() == {"message": "User testuser is authorized"}


