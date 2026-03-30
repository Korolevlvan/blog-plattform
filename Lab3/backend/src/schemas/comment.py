from datetime import datetime
from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    body: str = Field(min_length=1)


class CommentResponse(BaseModel):
    id: int
    body: str
    post_id: int
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
