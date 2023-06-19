from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Student, StudentUpdate,StudentCreate
from fastapi.responses import JSONResponse


app = FastAPI()

#根目录
@app.get("/")
async def root():
    return JSONResponse(content={"message": "欢迎访问我的学生信息管理API!"})

#查询所有学生信息
@app.get("/students")
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(Student).offset(skip).limit(limit).all()
    return students


# 更新学生信息
@app.put("/students/{student_id}")
async def update_student(student_id: int, student_update: StudentUpdate, db: Session = Depends(get_db)):
    # 查询指定 ID 的学生记录
    student = db.query(Student).filter(Student.id == student_id).first()

    # 如果找不到对应的学生，则返回错误响应
    if not student:
        raise HTTPException(status_code=404, detail="找不到指定的学生")

    # 更新学生信息
    for field, value in student_update.dict(exclude_unset=True).items():
        setattr(student, field, value)
    db.commit()

    return {"msg": "学生信息已更新"}

# 删除学生信息
@app.delete("/students/{student_id}")
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    # 查询指定 ID 的学生记录
    student = db.query(Student).filter(Student.id == student_id).first()

    # 如果找不到对应的学生，则返回错误响应
    if not student:
        raise HTTPException(status_code=404, detail="找不到指定的学生")

    # 删除学生记录
    db.delete(student)
    db.commit()

    return {"msg": "学生信息已删除"}

# 添加学生信息
@app.post("/students")
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # 创建学生记录
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return {"msg": "学生信息添加成功", "data": db_student}


# 查询某个学生信息的接口函数
@app.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="找不到指定的学生")
    return student

