from fastapi import FastAPI, Depends
from .models import Task
from .database import SessionLocal
from sqlalchemy.orm import Session
from . import crud

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


@app.post("/users/")
async def create_user(email: str, password: str, db: Session = Depends(get_db)):
    # you would actually hash the password here before creating a user with it
    hashed_password = password  # this is a placeholder, replace with actual hashing
    user = crud.create_user(db, email=email, hashed_password=hashed_password)
    return user