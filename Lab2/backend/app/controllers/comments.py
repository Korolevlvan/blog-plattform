from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.comment import Comment
from app.schemas.comment import CommentCreate

def create_comment(db: Session, article: Article, payload: CommentCreate, user_id: int) -> Comment:
    comment = Comment(body=payload.body, article_id=article.id, user_id=user_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def list_comments(db: Session, article: Article) -> list[Comment]:
    return list(
        db.scalars(
            select(Comment).where(Comment.article_id == article.id).order_by(Comment.created_at.asc())
        ).all()
    )

def get_comment(db: Session, comment_id: int) -> Comment | None:
    return db.scalar(select(Comment).where(Comment.id == comment_id))

def delete_comment(db: Session, comment: Comment) -> None:
    db.delete(comment)
    db.commit()
