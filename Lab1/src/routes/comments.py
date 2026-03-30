from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.controllers.articles import get_article_by_slug
from src.controllers.comments import create_comment, delete_comment, get_comment_by_id, list_comments
from src.db.session import get_db
from src.dependencies.auth import get_current_user
from src.models.user import User
from src.schemas.comment import CommentCreate, CommentRead

router = APIRouter(tags=["comments"])


@router.post(
    "/api/articles/{slug}/comments",
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_comment_route(
    slug: str,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CommentRead:
    article = get_article_by_slug(db, slug)
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    comment = create_comment(db, article, current_user, payload)
    return CommentRead.model_validate(comment)


@router.get("/api/articles/{slug}/comments", response_model=list[CommentRead])
def list_comments_route(slug: str, db: Session = Depends(get_db)) -> list[CommentRead]:
    article = get_article_by_slug(db, slug)
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return [CommentRead.model_validate(comment) for comment in list_comments(db, article)]


@router.delete("/api/articles/{slug}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment_route(
    slug: str,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    article = get_article_by_slug(db, slug)
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    comment = get_comment_by_id(db, article, comment_id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    delete_comment(db, comment)
