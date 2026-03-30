from datetime import datetime
from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1)
    tag_list: list[str] = Field(default_factory=list, alias="tagList")

    model_config = {"populate_by_name": True}


class PostResponse(BaseModel):
    id: int
    title: str
    description: str
    body: str
    slug: str
    user_id: int
    tag_list: list[str] = Field(alias="tagList")
    created_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}
