from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.dependencies import get_current_user
from ..models.comment import Comment
from ..models.article import Article
from ..models.user import User
from ..schemas.comment import CommentCreate, CommentOut

router = APIRouter(prefix="/api/articles/{slug}/comments", tags=["comments"])

def get_article_by_slug(slug: str, db: Session):
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.post("/", response_model=CommentOut)
def add_comment(slug: str, comment: CommentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    article = get_article_by_slug(slug, db)
    db_comment = Comment(body=comment.body, article_id=article.id, user_id=current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/", response_model=list[CommentOut])
def get_comments(slug: str, db: Session = Depends(get_db)):
    article = get_article_by_slug(slug, db)
    comments = db.query(Comment).filter(Comment.article_id == article.id).all()
    return comments

@router.delete("/{comment_id}")
def delete_comment(slug: str, comment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    article = get_article_by_slug(slug, db)
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.article_id == article.id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your comment")
    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted"}