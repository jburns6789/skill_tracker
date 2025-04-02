import strawberry
from typing import List
from app.models.models import Skill as SkillModel
from app.graphql.types import Skill, SkillInput
from sqlalchemy.orm import Session
from app.database import SessionLocal

#Query
@strawberry.type
class Query:
    @strawberry.field
    def skills(self) -> List[Skill]:
        db:Session = next(SessionLocal())
        skills = db.query(SkillModel).all()

        return [
            Skill(
                id=s.id,
                name=s.name,
                category_id=s.category_id,
                user_id=s.user_id
            )
            for s in skills
        ]
    
#Mutation
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_skill(self, input: SkillInput) -> Skill:
        db: Session = SessionLocal()
        new_skill = SkillModel(
            name=input.name,
            category_id=input.category_id,
            user_id=input.user_id
        )
        db.add(new_skill)
        db.commit()
        db.refresh(new_skill)

        return Skill(
            id=new_skill.id,
            name=new_skill.name,
            category_id=new_skill.category_id,
            user_id=new_skill.user.id
        )
    
schema = strawberry.Schema(query=Query, mutation=Mutation)