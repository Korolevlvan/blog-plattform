from sqlalchemy import Column, Integer, String, Text, ForeignKey
from ..core.database import Base

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=False)
    tag_list = Column(String, nullable=True)  # comma-separated