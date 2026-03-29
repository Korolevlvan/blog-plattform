from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.db import Base

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    slug = Column(String, unique=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    tag_list = Column(String, nullable=True)  # CSV строка для тегов

    author = relationship("User")