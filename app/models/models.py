from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password_hash = Column(String)

    skills = relationship("Skill", back_populates="user")

class SkillCategory(Base):
    __tablename__ = "skill_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    skills = relationship("Skill", back_populates="category")

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey("skill_categories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    category = relationship("SkillCategory", back_populates="skills")
    user = relationship("User", back_populates="skills")
    milestones = relationship("Milestone", back_populates="skill")

class Milestone(Base):
    __tablename__ = "milestones"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    date_achieved = Column(Date)
    skill_id = Column(Integer, ForeignKey("skills.id"))

    skill = relationship("Skill", back_populates="milestones")