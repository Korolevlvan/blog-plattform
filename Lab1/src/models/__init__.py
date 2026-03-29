from sqlalchemy.orm import declarative_base
from .user import User
from .database import Base
Base = declarative_base()