from app.schemas.skill import SkillCreate
from app.crud.skill import create_skill

class FakeDB:
    def __init__(self):
        self.data = []

    def add(self, obj):
        self.data.append(obj)

    def commit(self):
        pass

    def refresh(self, obj):
        obj.id = 1

def test_create_skill_directly():
    fake_db = FakeDB()
    skill = SkillCreate(name="UnitSkill", category_id=1, user_id=1)
    result = create_skill(fake_db, skill)
    assert result.name == "UnitSkill"
    assert result.category_id == 1
