from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.dependencies.auth import get_current_user
from src.models.user import User
from src.schemas.user import (
    SubscribeRequest,
    SubscriptionKeyUpdate,
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
    UserUpdate,
)
from src.services.users import login_user, register_user, subscribe_to_author, update_current_user, update_subscription_key

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user_route(payload: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, payload)


@router.post("/users/login", response_model=TokenResponse)
def login_user_route(payload: UserLogin, db: Session = Depends(get_db)):
    token = login_user(db, payload)
    return TokenResponse(access_token=token)


@router.get("/user", response_model=UserResponse)
def current_user_route(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/user", response_model=UserResponse)
def update_user_route(payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_current_user(db, current_user, payload)


@router.put("/users/me/subscription-key", response_model=UserResponse)
def update_subscription_key_route(
    payload: SubscriptionKeyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_subscription_key(db, current_user, payload)


@router.post("/users/subscribe", status_code=status.HTTP_204_NO_CONTENT)
def subscribe_route(
    payload: SubscribeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    subscribe_to_author(db, current_user, payload)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
