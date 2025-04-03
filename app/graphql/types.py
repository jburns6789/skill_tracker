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

@strawberry.input
class SkillUpdateInput:
    id: int
    name: str
    user_id: int

@strawberry.input
class SkillDelete:
    id: int



#strawberry.type -> output/responses
#strawberry.input -> input/mutations