from database import Base, SessionLocal

from sqlalchemy import Column, Integer, String

class Post(Base):
    __tablename__ = 'post'
    __table_args__ = {"schema": "cd"}

    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)


if __name__ == '__main__':
    with SessionLocal() as db:
        results = db.query(Post)\
            .filter(Post.topic == 'business')\
            .order_by(Post.id.desc())\
            .limit(10)\
            .all()
        print([
            res.id
            for res in results
        ])

        
