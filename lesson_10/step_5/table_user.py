from database import Base, SessionLocal

from sqlalchemy import Column, Integer, String, func
from sqlalchemy.sql import text

class User(Base):
    __tablename__ = 'user'

    age = Column(Integer)
    city = Column(String)
    country = Column(String)
    exp_group = Column(Integer)
    gender = Column(Integer)
    id = Column(Integer, primary_key=True)
    os = Column(String)
    source = Column(String)

if __name__ == '__main__':
    with SessionLocal() as db:
        results = db.query(
            User.country,
            User.os,
            func.count().label('cnt')
            )\
            .filter(User.exp_group == 3)\
            .group_by(User.country, User.os)\
            .having(func.count() > 100)\
            .order_by(text("cnt desc"))\
            .all()
        
        print([
            (res.country, res.os, res.cnt)
            for res in results
        ])