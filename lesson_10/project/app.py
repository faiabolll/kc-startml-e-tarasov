from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import text
from sqlalchemy import desc, func


from table_user import User
from table_post import Post
from table_feed import Feed

from schema import *
from typing import List

from database import SessionLocal

app = FastAPI()

def get_db():
    with SessionLocal() as db:
        return db

@app.get("/user/{id}", response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db)):
    result = db.query(User).filter(User.id == id).first()
    if result is None:
        raise HTTPException(404, "Not found")
    else:
        return result
        
@app.get("/post/{id}", response_model=PostGet)
def get_post(id: int, db: Session = Depends(get_db)):
    result = db.query(Post).filter(Post.id == id).first()
    if result is None:
        raise HTTPException(404, "Not found")
    else:
        return result
    
    
    
@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_user_feed(id: int, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed).filter(Feed.user_id == id).order_by(desc(Feed.time)).limit(limit).all()
    return result

@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_post_feed(id: int, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed).filter(Feed.post_id == id).order_by(desc(Feed.time)).limit(limit).all()
    return result


@app.get('/post/recommendations/', response_model=List[PostGet])
def get_recommendations(id: int = None, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(
        Post
    ).select_from(Feed)\
    .filter(Feed.action == 'like')\
    .join(Post)\
    .group_by(Post.id)\
    .order_by(desc(func.count(Post.id)))\
    .limit(limit)\
    .all()
    return result
