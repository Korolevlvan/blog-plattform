from pydantic import BaseModel

class CommentBase(BaseModel):
    body: str

class CommentCreate(CommentBase):
    pass

class CommentOut(CommentBase):
    id: int
    user_id: int
    article_id: int

    class Config:
        from_attributes = True