from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class CommentCreate(BaseModel):
    body: str = Field(min_length=1)

class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    body: str
    article_id: int
    user_id: int
    created_at: datetime
