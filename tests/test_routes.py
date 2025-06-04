import pytest
from fastapi import status
from sqlalchemy import select
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
    assert "authorized" in response.json()["message"]

@pytest.mark.asyncio
async def test_add_skill(async_client, test_db):
    response = await async_client.post(
        "/skills",
        json={"name": "FastAPI Skill Up", "category_id": 1}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["name"] == "FastAPI Skill Up"
    # Use async query
    result = await test_db.execute(select(Skill).where(Skill.id == data["id"]))
    skill = result.scalars().first()
    assert skill is not None
    assert skill.name == "FastAPI Skill Up"

@pytest.mark.asyncio
async def test_get_skill(async_client, test_db):
    # Create test skill first
    create_response = await async_client.post(
        "/skills",
        json={"name": "Test Skill", "category_id": 1}
    )
    # Get skills
    response = await async_client.get("/skills")
    assert response.status_code == 200
    skills = response.json()
    assert len(skills) >= 1
    assert any(s["name"] == "Test Skill" for s in skills)

@pytest.mark.asyncio
async def test_put_skill(async_client, test_db):
    # Create
    create_res = await async_client.post(
        "/skills",
        json={"name": "Original Skill", "category_id": 1}
    )
    skill_id = create_res.json()["id"]
    # Update
    update_res = await async_client.put(
        f"/skills/{skill_id}",
        json={"name": "Updated Skill Name"}
    )
    assert update_res.status_code == 201
    assert update_res.json()["name"] == "Updated Skill Name"
    # Verify
    result = await test_db.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalars().first()
    assert skill.name == "Updated Skill Name"

@pytest.mark.asyncio
async def test_delete_skill(async_client, test_db):
    # Create
    create_res = await async_client.post(
        "/skills",
        json={"name": "To Delete", "category_id": 1}
    )
    skill_id = create_res.json()["id"]
    # Delete
    delete_res = await async_client.delete(f"/skills/{skill_id}")
    assert delete_res.status_code == 200
    # Verify
    result = await test_db.execute(select(Skill).where(Skill.id == skill_id))
    assert result.scalars().first() is None
