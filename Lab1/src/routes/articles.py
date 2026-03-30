from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.controllers.articles import (
    create_article,
    delete_article,
    get_article_by_slug,
    list_articles,
    update_article,
)
from src.db.session import get_db
from src.dependencies.auth import get_current_user
from src.models.user import User
from src.schemas.article import ArticleCreate, ArticleRead, ArticleUpdate

router = APIRouter(tags=["articles"])


def _to_schema(article) -> ArticleRead:
    return ArticleRead(
        slug=article.slug,
        title=article.title,
        description=article.description,
        body=article.body,
        tagList=article.tag_list,
        author_id=article.author_id,
    )


@router.post("/api/articles", response_model=ArticleRead, status_code=status.HTTP_201_CREATED)
def create_article_route(
    payload: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ArticleRead:
    article = create_article(db, current_user, payload)
    return _to_schema(article)


@router.get("/api/articles", response_model=list[ArticleRead])
def list_articles_route(db: Session = Depends(get_db)) -> list[ArticleRead]:
    return [_to_schema(article) for article in list_articles(db)]


@router.get("/api/articles/{slug}", response_model=ArticleRead)
def get_article_route(slug: str, db: Session = Depends(get_db)) -> ArticleRead:
    article = get_article_by_slug(db, slug)
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return _to_schema(article)


@router.put("/api/articles/{slug}", response_model=ArticleRead)
def update_article_route(
    slug: str,
    payload: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ArticleRead:
    article = get_article_by_slug(db, slug)
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    if article.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    article = update_article(db, article, payload)
    return _to_schema(article)


@router.delete("/api/articles/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article_route(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    article = get_article_by_slug(db, slug)
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    if article.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    delete_article(db, article)
