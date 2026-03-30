from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class ArticleCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=500)
    body: str = Field(min_length=1)
    tagList: list[str] = Field(default_factory=list)

class ArticleUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1, max_length=500)
    body: str | None = Field(default=None, min_length=1)
    tagList: list[str] | None = None

class ArticleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    body: str
    slug: str
    user_id: int
    tag_list: list[str]
    created_at: datetime
    updated_at: datetime
