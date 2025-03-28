from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_skill():
    response = client.post(
        "/skills",
        json={
            "name": "TestingSkill",
            "category_id": 1,
            "user_id": 1,
        }
    )
    assert response.status_code ==200
    data = response.json()
    assert data["name"] == "TestingSkill"
    assert data["category_id"] == 1
    assert "id" in data

#Makes sure the skill is created successfully and the response is structured as expected