from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import verify_password, get_password_hash, create_access_token
from ..core.dependencies import get_current_user
from ..models.user import User
from ..schemas.user import UserCreate, UserOut, UserLogin, Token, UserUpdate
from fastapi import Form
router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    hashed = get_password_hash(user.password)
    db_user = User(email=user.email, username=user.username, hashed_password=hashed, bio=user.bio, image_url=user.image_url)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from fastapi import Form

@router.post("/login", response_model=Token)
def login(
    username: str = Form(...),   # это будет email
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == username).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": token}

@router.get("/me", response_model=UserOut)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserOut)
def update_current_user(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    for field, value in user_update.dict(exclude_unset=True).items():
        if field == "password" and value:
            setattr(current_user, "hashed_password", get_password_hash(value))
        elif field != "password":
            setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user