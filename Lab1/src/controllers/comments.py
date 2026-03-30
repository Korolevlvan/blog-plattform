from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.article import Article
from src.models.comment import Comment
from src.models.user import User
from src.schemas.comment import CommentCreate


def create_comment(db: Session, article: Article, author: User, payload: CommentCreate) -> Comment:
    comment = Comment(body=payload.body, article_id=article.id, author_id=author.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def list_comments(db: Session, article: Article) -> list[Comment]:
    return list(
        db.scalars(select(Comment).where(Comment.article_id == article.id).order_by(Comment.id.desc())).all()
    )


def get_comment_by_id(db: Session, article: Article, comment_id: int) -> Comment | None:
    return db.scalar(
        select(Comment).where(Comment.article_id == article.id, Comment.id == comment_id)
    )


def delete_comment(db: Session, comment: Comment) -> None:
    db.delete(comment)
    db.commit()
