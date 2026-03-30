from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1)
    bio: str | None = None
    image_url: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None
    bio: str | None = None
    image_url: str | None = None


class SubscriptionKeyUpdate(BaseModel):
    subscription_key: str = Field(min_length=1)


class SubscribeRequest(BaseModel):
    target_user_id: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    bio: str | None = None
    image_url: str | None = None
    subscription_key: str | None = None

    model_config = {"from_attributes": True}
