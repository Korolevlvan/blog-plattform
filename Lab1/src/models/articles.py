from sqlalchemy import Column, Integer, String, Text, ForeignKey
from src.models import Base
from sqlalchemy.orm import relationship

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    body = Column(Text)
    tagList = Column(String, nullable=True)
    slug = Column(String, unique=True, index=True)

    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article")
