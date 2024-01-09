from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .table_user import User
from .schema import *

from database import SessionLocal

app = FastAPI()

def get_db():
    with SessionLocal() as db:
        return db

@app.get("/user/{id}")
def get_user(id: int, db: Session = Depends(get_db), response_model=UserGet):
    return db.query(User).filter(User.id == id).limit(1).one()

@app.get("/post/{id}")
def get_post(id: int, db: Session = Depends(get_db), response_model=PostGet):
    return db.query(User).filter(User.id == id).limit(1).one()