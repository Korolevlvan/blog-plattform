from sqlalchemy import select
from sqlalchemy.orm import Session
from slugify import slugify

from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate

def _generate_unique_slug(db: Session, title: str) -> str:
    base_slug = slugify(title)
    slug = base_slug or "article"
    index = 1
    while db.scalar(select(Article).where(Article.slug == slug)) is not None:
        index += 1
        slug = f"{base_slug}-{index}"
    return slug

def create_article(db: Session, payload: ArticleCreate, user_id: int) -> Article:
    article = Article(
        title=payload.title,
        description=payload.description,
        body=payload.body,
        slug=_generate_unique_slug(db, payload.title),
        user_id=user_id,
        tag_list=payload.tagList,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

def list_articles(db: Session) -> list[Article]:
    return list(db.scalars(select(Article).order_by(Article.created_at.desc())).all())

def get_article_by_slug(db: Session, slug: str) -> Article | None:
    return db.scalar(select(Article).where(Article.slug == slug))

def update_article(db: Session, article: Article, payload: ArticleUpdate) -> Article:
    if payload.title is not None and payload.title != article.title:
        article.title = payload.title
        article.slug = _generate_unique_slug(db, payload.title)
    if payload.description is not None:
        article.description = payload.description
    if payload.body is not None:
        article.body = payload.body
    if payload.tagList is not None:
        article.tag_list = payload.tagList
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

def delete_article(db: Session, article: Article) -> None:
    db.delete(article)
    db.commit()
