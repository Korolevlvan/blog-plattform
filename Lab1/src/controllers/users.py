from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from src.core.security import create_access_token, hash_password, verify_password
from src.models.user import User
from src.schemas.user import TokenResponse, UserCreate, UserUpdate


def register_user(db: Session, payload: UserCreate) -> User:
    existing = db.scalar(
        select(User).where(or_(User.email == payload.email, User.username == payload.username))
    )
    if existing:
        raise ValueError("User with this email or username already exists")

    user = User(
        email=str(payload.email),
        username=payload.username,
        hashed_password=hash_password(payload.password),
        bio=payload.bio,
        image_url=payload.image_url,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == str(email)))
    if user is None or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid email or password")

    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)


def update_current_user(db: Session, user: User, payload: UserUpdate) -> User:
    if payload.email and payload.email != user.email:
        existing_email = db.scalar(select(User).where(User.email == str(payload.email)))
        if existing_email and existing_email.id != user.id:
            raise ValueError("Email already in use")
        user.email = str(payload.email)

    if payload.username and payload.username != user.username:
        existing_username = db.scalar(select(User).where(User.username == payload.username))
        if existing_username and existing_username.id != user.id:
            raise ValueError("Username already in use")
        user.username = payload.username

    if payload.password:
        user.hashed_password = hash_password(payload.password)
    if payload.bio is not None:
        user.bio = payload.bio
    if payload.image_url is not None:
        user.image_url = payload.image_url

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
