from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db import get_db
from src.controllers.article_controller import create_article, get_articles, get_article_by_slug, update_article, delete_article

router = APIRouter()

@router.post("/articles")
def create_article_route(article: dict, db: Session = Depends(get_db)):
    return create_article(db, article["title"], article["description"], article["body"], author_id=1, tag_list=article.get("tagList"))

@router.get("/articles")
def list_articles(db: Session = Depends(get_db)):
    return get_articles(db)

@router.get("/articles/{slug}")
def get_article(slug: str, db: Session = Depends(get_db)):
    article = get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.put("/articles/{slug}")
def update_article_route(slug: str, data: dict, db: Session = Depends(get_db)):
    article = update_article(db, slug, data)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.delete("/articles/{slug}")
def delete_article_route(slug: str, db: Session = Depends(get_db)):
    article = delete_article(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "Deleted"}