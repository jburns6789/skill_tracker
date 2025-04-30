import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

from app.api.routes import get_db
from app.auth.dependencies import get_current_user
from app.models.models import User
from app.database import SessionLocal

from app.models.models import Skill


@pytest.mark.asyncio
async def test_root(async_client):
        response = await async_client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "SkillTree API is working!"}

@pytest.mark.asyncio
async def test_whoami(async_client):
        response = await async_client.get("/whoami")
        assert response.status_code == 200
        assert response.json() == {"message": "User testuser is authorized"}

@pytest.mark.asyncio
async def test_add_skill(async_client, test_db):
    response = await async_client.post(
        "/skills",
        json={
             "name": "FastAPI Skill Up", "category_id": 1}
        )
        
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    
    skill = test_db.query(Skill).get(data["id"])
    assert skill is not None
    assert skill.name == "FastAPI Skill Up"
    assert skill.user_id == 1

# @pytest.mark.asyncio
# async def test_get_skill():
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as ac:
#         response = await ac.get("/skills")
#         assert response.status_code == 200

# @pytest.mark.asyncio
# async def test_put_skill():
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as ac:
#         response = await ac.get("/skills")
#         assert response.status_code == 200

# @pytest.mark.asyncio
# async def test_delete_skill():
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as ac:
#         response = await ac.get("/skills")
#         assert response.status_code == 200
