from sqlalchemy import Column, Integer, String, Float
from database import Base
from pydantic import BaseModel

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    age = Column(Integer, nullable=False)
    classname = Column(String(64), nullable=False)
    course_a = Column(Integer, nullable=False)
    course_b = Column(Integer, nullable=False)
    course_c = Column(Integer, nullable=False)

class StudentUpdate(BaseModel):
    name: str = None
    age: int = None
    classname: str = None
    course_a: int = None
    course_b: int = None
    course_c: int = None

    class Config:
        orm_mode = True

class StudentCreate(BaseModel):
    name: str
    age: int
    classname: str
    course_a: int
    course_b: int
    course_c: int

    class Config:
        orm_mode = True