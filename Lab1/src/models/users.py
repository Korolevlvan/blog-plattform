from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.models import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    bio = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)

    articles = relationship("Article", back_populates="owner")
