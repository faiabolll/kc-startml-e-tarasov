from database import Base
from datetime import datetime

from sqlalchemy import Column, Integer, String, func, ForeignKey
from sqlalchemy.sql import text

class Feed(Base):
    __tablename__ = 'feed_action'
    __table_args__ = {"schema": "cd"}

    action = Column(String)
    post_id = Column(String, ForeignKey("cd.post.id"))
    time = Column(datetime)
    user_id = Column(String, ForeignKey("cd.user.id"))