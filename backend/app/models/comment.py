from sqlalchemy import Column, Integer, String, Text, ForeignKey
from ..core.database import Base

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text, nullable=False)
    article_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)