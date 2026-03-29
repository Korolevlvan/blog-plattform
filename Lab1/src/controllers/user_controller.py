from sqlalchemy.orm import Session
from src.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, email, username, password):
    max_len = 72
    if len(password.encode('utf-8')) > max_len:
        password = password.encode('utf-8')[:max_len].decode('utf-8', 'ignore')
    hashed_password = pwd_context.hash(password)
    user = User(email=email, username=username, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email, password):
    user = db.query(User).filter(User.email == email).first()
    if user and pwd_context.verify(password, user.password):
        return user
    return None