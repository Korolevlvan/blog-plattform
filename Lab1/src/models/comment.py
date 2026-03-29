from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.db import Base

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String, nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"))
    author_id = Column(Integer, ForeignKey("users.id"))

    article = relationship("Article")
    author = relationship("User")