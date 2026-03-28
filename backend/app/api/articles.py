from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user_id
from ..models.article import Article
from ..models.user import User
from ..schemas.article import ArticleCreate, ArticleUpdate, ArticleOut
from ..utils.slugify import generate_slug

router = APIRouter(prefix="/api/articles", tags=["articles"])

def get_article_by_slug(slug: str, db: Session):
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.post("/", response_model=ArticleOut)
def create_article(article: ArticleCreate, current_user: User = Depends(get_current_user_id), db: Session = Depends(get_db)):
    slug = generate_slug(article.title)
    # check if slug already exists
    if db.query(Article).filter(Article.slug == slug).first():
        slug = f"{slug}-{db.query(Article).count() + 1}"
    tag_list = ",".join(article.tagList) if article.tagList else None
    db_article = Article(
        title=article.title,
        slug=slug,
        description=article.description,
        body=article.body,
        user_id=current_user_id,
        tag_list=tag_list
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.get("/", response_model=list[ArticleOut])
def list_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()

@router.get("/{slug}", response_model=ArticleOut)
def get_article(slug: str, db: Session = Depends(get_db)):
    return get_article_by_slug(slug, db)

@router.put("/{slug}", response_model=ArticleOut)
def update_article(slug: str, article_update: ArticleUpdate, current_user: User = Depends(get_current_user_id), db: Session = Depends(get_db)):
    db_article = get_article_by_slug(slug, db)
    if db_article.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not your article")
    for field, value in article_update.dict(exclude_unset=True).items():
        if field == "tagList":
            setattr(db_article, "tag_list", ",".join(value) if value else None)
        elif field != "slug":
            setattr(db_article, field, value)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.delete("/{slug}")
def delete_article(slug: str, current_user: User = Depends(get_current_user_id), db: Session = Depends(get_db)):
    db_article = get_article_by_slug(slug, db)
    if db_article.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not your article")
    db.delete(db_article)
    db.commit()
    return {"detail": "Article deleted"}