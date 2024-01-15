from database import Base, SessionLocal
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from table_user import User
from table_post import Post

class Feed(Base):
    __tablename__ = 'feed_action'
    __table_args__ = {"schema": "public"}
    
    action = Column(String)
    post_id = Column(Integer, ForeignKey(Post.id), primary_key=True)
    time = Column(DateTime(timezone=False))
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    
    user = relationship(User)
    post = relationship(Post)