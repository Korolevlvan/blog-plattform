from pydantic import BaseModel, ConfigDict


class ArticleCreate(BaseModel):
    title: str
    description: str
    body: str
    tagList: list[str] | None = None


class ArticleUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    body: str | None = None
    tagList: list[str] | None = None


class ArticleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slug: str
    title: str
    description: str
    body: str
    tagList: list[str]
    author_id: int
