from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db import get_db
from src.controllers.comment_controller import create_comment, get_comments, delete_comment

router = APIRouter()

@router.post("/articles/{slug}/comments")
def add_comment(slug: str, comment: dict, db: Session = Depends(get_db)):
    article = db.query(db.tables["articles"]).filter_by(slug=slug).first()
    if not article:
        return {"error": "Article not found"}
    return create_comment(db, article.id, 1, comment["body"])

@router.get("/articles/{slug}/comments")
def list_comments(slug: str, db: Session = Depends(get_db)):
    article = db.query(db.tables["articles"]).filter_by(slug=slug).first()
    if not article:
        return {"error": "Article not found"}
    return get_comments(db, article.id)

@router.delete("/articles/{slug}/comments/{id}")
def remove_comment(slug: str, id: int, db: Session = Depends(get_db)):
    return delete_comment(db, id)