import strawberry
from typing import List
from app.models.models import Skill as SkillModel
from app.graphql.types import Skill, SkillInput, SkillUpdateInput, SkillDelete
from sqlalchemy.orm import Session
from app.database import AsyncSessionLocal

from strawberry.types import Info
from app.auth.jwt import decode_access_token

#Query
@strawberry.type
class Query:
    @strawberry.field
    def skills(self, info: Info) -> List[Skill]:
        request = info.context["request"]
        token = request.headers.get("Authorization")
                                    
        if not token or not token.startswith("Bearer "):
            raise Exception("Unauthorized")
        
        payload = decode_access_token(token.split(" ")[1])
        if not payload:
            raise Exception("Invalid or expired token")
        
        user_id = int(payload["sub"])
        db: Session = AsyncSessionLocal()
        try:
            skills = db.query(SkillModel).filter(SkillModel.user_id == user_id).all()
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



# Not authenticated
# @strawberry.type
# class Query:
#     @strawberry.field
#     def skills(self) -> List[Skill]:
#         db:Session = SessionLocal()
#         try:
#             skills = db.query(SkillModel).all()

#             return [
#                 Skill(
#                     id=s.id,
#                     name=s.name,
#                     category_id=s.category_id,
#                     user_id=s.user_id
#                 )
#                 for s in skills
#             ]
#         finally:
#             db.close()
    

#Mutation
@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_skill(self, input: SkillInput) -> Skill:
        db: Session = AsyncSessionLocal()
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
                user_id=new_skill.user_id
            )
        finally:
            db.close()


    @strawberry.mutation
    def update_skill(self, input: SkillUpdateInput) -> Skill:
        db: Session = AsyncSessionLocal()
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
                user_id=skill.user_id
            )
        finally:
            db.close()


    @strawberry.mutation    
    def delete_skill(self, id: int) -> bool:
        db: Session = AsyncSessionLocal()
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

@strawberry.field
def skills(self, info: Info) -> List[Skill]:
    request = info.context["request"]
    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        raise Exception("Unauthorized")
    
    payload = decode_access_token(token.split(" ")[1])
    if not payload:
        raise Exception("Invalid or expired token")
    
    user_id = payload["sub"]

    db: Session = Session()

    try:
        skills = db.query(SkillModel).filter(SkillModel.user_id == user_id).all()
        return [Skill()]
    finally:
        db.close()


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

  

