from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controllers.articles import create_article, delete_article, get_article_by_slug, list_articles, update_article
from app.core.security import get_current_user_id
from app.db.session import get_db
from app.schemas.article import ArticleCreate, ArticleOut, ArticleUpdate

router = APIRouter(tags=["articles"])

@router.post("/api/articles", response_model=ArticleOut, status_code=status.HTTP_201_CREATED)
@router.post("/api/posts", response_model=ArticleOut, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_article_endpoint(
    payload: ArticleCreate,
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    return create_article(db, payload, user_id)

@router.get("/api/articles", response_model=list[ArticleOut])
@router.get("/api/posts", response_model=list[ArticleOut], include_in_schema=False)
def list_articles_endpoint(db: Annotated[Session, Depends(get_db)]):
    return list_articles(db)

@router.get("/api/articles/{slug}", response_model=ArticleOut)
@router.get("/api/posts/{slug}", response_model=ArticleOut, include_in_schema=False)
def get_article_endpoint(slug: str, db: Annotated[Session, Depends(get_db)]):
    article = get_article_by_slug(db, slug)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.put("/api/articles/{slug}", response_model=ArticleOut)
@router.put("/api/posts/{slug}", response_model=ArticleOut, include_in_schema=False)
def update_article_endpoint(
    slug: str,
    payload: ArticleUpdate,
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    article = get_article_by_slug(db, slug)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can update only your own article")
    return update_article(db, article, payload)

@router.delete("/api/articles/{slug}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/api/posts/{slug}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_article_endpoint(
    slug: str,
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    article = get_article_by_slug(db, slug)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can delete only your own article")
    delete_article(db, article)
