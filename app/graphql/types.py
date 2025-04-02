import strawberry

@strawberry.type
class Skill:
    id:int
    name: str
    category_id: int
    user_id: int

@strawberry.input
class SkillInput:
    name: str
    category_id: int
    user_id: int