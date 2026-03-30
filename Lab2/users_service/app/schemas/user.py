from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=6, max_length=200)
    bio: str | None = None
    image_url: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = Field(default=None, min_length=1, max_length=255)
    password: str | None = Field(default=None, min_length=6, max_length=200)
    bio: str | None = None
    image_url: str | None = None

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    bio: str | None
    image_url: str | None
    created_at: datetime
    updated_at: datetime

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
