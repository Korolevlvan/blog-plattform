from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    body: str


class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    body: str
    article_id: int
    author_id: int
