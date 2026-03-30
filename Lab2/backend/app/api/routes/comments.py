from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controllers.articles import get_article_by_slug
from app.controllers.comments import create_comment, delete_comment, get_comment, list_comments
from app.core.security import get_current_user_id
from app.db.session import get_db
from app.schemas.comment import CommentCreate, CommentOut

router = APIRouter(tags=["comments"])

@router.post("/api/articles/{slug}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
@router.post("/api/posts/{slug}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_comment_endpoint(
    slug: str,
    payload: CommentCreate,
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    article = get_article_by_slug(db, slug)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return create_comment(db, article, payload, user_id)

@router.get("/api/articles/{slug}/comments", response_model=list[CommentOut])
@router.get("/api/posts/{slug}/comments", response_model=list[CommentOut], include_in_schema=False)
def list_comments_endpoint(slug: str, db: Annotated[Session, Depends(get_db)]):
    article = get_article_by_slug(db, slug)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return list_comments(db, article)

@router.delete("/api/articles/{slug}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/api/posts/{slug}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_comment_endpoint(
    slug: str,
    comment_id: int,
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    article = get_article_by_slug(db, slug)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    comment = get_comment(db, comment_id)
    if comment is None or comment.article_id != article.id:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can delete only your own comment")
    delete_comment(db, comment)
