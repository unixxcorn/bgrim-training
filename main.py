from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from database import SessionLocal, Base, engine
from models import Task, User

app = FastAPI()
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Routes for User operations
@app.post("/users/")
def create_user(email: str, password: str, db: Session = Depends(get_db)):
    hashed_password = password  # placeholder: add hashing
    new_user = User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, email: str, password: str, is_active: bool, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.email = email  # For simplicity, no checks are done here. In real scenarios, validate changes.
    user.hashed_password = password  # placeholder: add hashing
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}

# Routes for Task operations
@app.post("/users/{user_id}/tasks/")
def create_task(user_id: int, title: str, description: str, db: Session = Depends(get_db)):
    new_task = Task(title=title, description=description, owner_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str, description: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = title
    task.description = description
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}

# New route for listing all users
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# New route for listing all tasks
@app.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# New route for listing all tasks of a specific user
@app.get("/users/{user_id}/tasks/")
def read_user_tasks(user_id: int, db: Session = Depends(get_db)):
    # This will only retrieve the tasks for a specific user. 
    # You may want to add error handling to ensure the user_id is valid.
    tasks = db.query(Task).filter(Task.owner_id == user_id).all()
    return tasks


