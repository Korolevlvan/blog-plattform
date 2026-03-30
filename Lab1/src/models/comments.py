from sqlalchemy import Column, Integer, Text, ForeignKey
from src.models import Base
from sqlalchemy.orm import relationship

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text)

    article_id = Column(Integer, ForeignKey('articles.id'))
    article = relationship("Article", back_populates="comments")
