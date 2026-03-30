from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.dependencies.auth import get_current_user_id
from src.schemas.comment import CommentCreate, CommentResponse
from src.services.comments import create_comment, list_comments

router = APIRouter()


@router.post("/posts/{slug}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
@router.post("/articles/{slug}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_comment_route(slug: str, payload: CommentCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return create_comment(db, slug, payload, current_user_id)


@router.get("/posts/{slug}/comments", response_model=list[CommentResponse])
@router.get("/articles/{slug}/comments", response_model=list[CommentResponse], include_in_schema=False)
def list_comments_route(slug: str, db: Session = Depends(get_db)):
    return list_comments(db, slug)
