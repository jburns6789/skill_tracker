from fastapi.testclient import TestClient
from app.main import app
from app.api.routes import get_db
from app.auth.dependencies import get_current_user
from app.models.models import User
from app.database import SessionLocal

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

client = TestClient(app)

def test_create_skill():
    response = client.post(
        "/skills",
        json={
            "name": "TestingSkill",
            "category_id": 1,
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TestingSkill"
    assert data["category_id"] == 1
    assert "id" in data

#Makes sure the skill is created successfully and the response is structured as expected