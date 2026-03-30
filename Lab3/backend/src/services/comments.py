from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.article import Post
from src.models.comment import Comment
from src.schemas.comment import CommentCreate


def create_comment(db: Session, slug: str, payload: CommentCreate, author_id: int) -> Comment:
    post = db.scalar(select(Post).where(Post.slug == slug))
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    comment = Comment(body=payload.body, post_id=post.id, user_id=author_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def list_comments(db: Session, slug: str) -> list[Comment]:
    post = db.scalar(select(Post).where(Post.slug == slug))
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return list(db.scalars(select(Comment).where(Comment.post_id == post.id).order_by(Comment.id.asc())).all())
