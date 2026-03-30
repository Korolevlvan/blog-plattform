from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.scalar(select(User).where(User.username == username))

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.scalar(select(User).where(User.id == user_id))

def ensure_unique_fields(db: Session, email: str, username: str, ignore_user_id: int | None = None) -> None:
    stmt = select(User).where(or_(User.email == email, User.username == username))
    if ignore_user_id is not None:
        stmt = stmt.where(User.id != ignore_user_id)
    existing = db.scalar(stmt)
    if existing is None:
        return
    if existing.email == email:
        raise ValueError("Email already registered")
    raise ValueError("Username already taken")

def create_user(db: Session, payload: UserCreate) -> User:
    ensure_unique_fields(db, payload.email, payload.username)
    user = User(
        email=payload.email,
        username=payload.username,
        password_hash=hash_password(payload.password),
        bio=payload.bio,
        image_url=payload.image_url,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if user is None:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def update_user(db: Session, user: User, payload: UserUpdate) -> User:
    new_email = payload.email or user.email
    new_username = payload.username or user.username
    ensure_unique_fields(db, new_email, new_username, ignore_user_id=user.id)

    user.email = new_email
    user.username = new_username
    if payload.password:
        user.password_hash = hash_password(payload.password)
    if payload.bio is not None:
        user.bio = payload.bio
    if payload.image_url is not None:
        user.image_url = payload.image_url

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
