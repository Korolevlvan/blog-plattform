from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.security import create_access_token, hash_password, verify_password
from src.models.subscriber import Subscriber
from src.models.user import User
from src.schemas.user import SubscribeRequest, SubscriptionKeyUpdate, UserLogin, UserRegister, UserUpdate


def register_user(db: Session, payload: UserRegister) -> User:
    existing = db.scalar(select(User).where(or_(User.email == payload.email, User.username == payload.username)))
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email or username already exists")

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


def login_user(db: Session, payload: UserLogin) -> str:
    user = db.scalar(select(User).where(User.email == payload.email))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return create_access_token(user.id)


def update_current_user(db: Session, user: User, payload: UserUpdate) -> User:
    if payload.email is not None:
        user.email = payload.email
    if payload.username is not None:
        user.username = payload.username
    if payload.password is not None:
        user.password_hash = hash_password(payload.password)
    if payload.bio is not None:
        user.bio = payload.bio
    if payload.image_url is not None:
        user.image_url = payload.image_url

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_subscription_key(db: Session, user: User, payload: SubscriptionKeyUpdate) -> User:
    user.subscription_key = payload.subscription_key
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def subscribe_to_author(db: Session, user: User, payload: SubscribeRequest) -> None:
    if payload.target_user_id == user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot subscribe to yourself")

    target = db.scalar(select(User).where(User.id == payload.target_user_id))
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target user not found")

    relation = Subscriber(subscriber_id=user.id, author_id=payload.target_user_id)
    db.add(relation)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
