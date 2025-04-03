import strawberry
from typing import List
from app.models.models import Skill as SkillModel
from app.graphql.types import Skill, SkillInput, SkillUpdateInput, SkillDelete
from sqlalchemy.orm import Session
from app.database import SessionLocal

#Query
@strawberry.type
class Query:
    @strawberry.field
    def skills(self) -> List[Skill]:
        db:Session = SessionLocal()
        try:
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
        finally:
            db.close()
    

#Mutation
@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_skill(self, input: SkillInput) -> Skill:
        db: Session = SessionLocal()
        try:
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
        finally:
            db.close()


    @strawberry.mutation
    def update_skill(self, input: SkillUpdateInput) -> Skill:
        db: Session = SessionLocal()
        try:
            skill = db.query(SkillModel).filter(SkillModel.id == input.id).first()

            if not skill:
                raise Exception(f"Skill with id {input.id} not found")
            
            skill.name = input.name
            db.commit()
            db.refresh(skill)

            return Skill(
                id=skill.id,
                name=skill.name,
                category_id=skill.category_id,
                user_id=skill.user.id
            )
        finally:
            db.close()


    @strawberry.mutation    
    def delete_skill(self, id: int) -> bool:
        db: Session = SessionLocal()
        try:
            skill = db.query(SkillModel).filter(SkillModel.id == id).first()
            if not skill:
                return False
        
            db.delete(skill)
            db.commit()
            return True
        finally:
            db.close()
        
schema = strawberry.Schema(query=Query, mutation=Mutation)




# browswer testing
# mutation {
#   updateSkill(input: {
#     id: 13
#     name: "Cracking the Code 2"
#     userId: 1
#   }) {
#     id
#     name
#     userId
#     categoryId
#   }
# }

# mutation {
#   deleteSkill(id: 3)
# }

  

