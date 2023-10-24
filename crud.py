from sqlalchemy.orm import Session
from . import models  # adjust the import according to your project structure

# CRUD for the User model
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, email: str, hashed_password: str):
    new_user = models.User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user_id: int, new_email: str = None, new_hashed_password: str = None, new_is_active: bool = None):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        return None  # Not found

    if new_email:
        user.email = new_email
    if new_hashed_password:
        user.hashed_password = new_hashed_password
    if new_is_active is not None:  # considering that is_active flag might be 'False', which shouldn't be ignored
        user.is_active = new_is_active

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        return None  # Not found
    
    db.delete(user)
    db.commit()
    return user

# CRUD for the Task model
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks_by_owner(db: Session, owner_id: int):
    return db.query(models.Task).filter(models.Task.owner_id == owner_id).all()

def create_task(db: Session, title: str, description: str, owner_id: int):
    new_task = models.Task(title=title, description=description, owner_id=owner_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def update_task(db: Session, task_id: int, new_title: str = None, new_description: str = None):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        return None  # Not found

    if new_title:
        task.title = new_title
    if new_description:
        task.description = new_description

    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        return None  # Not found

    db.delete(task)
    db.commit()
    return task
