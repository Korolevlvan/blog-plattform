from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.dependencies.auth import get_current_user_id
from src.schemas.article import PostCreate, PostResponse
from src.services.articles import create_post, get_post_by_slug, list_posts

router = APIRouter()


@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
@router.post("/articles", response_model=PostResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_post_route(payload: PostCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return create_post(db, payload, current_user_id)


@router.get("/posts", response_model=list[PostResponse])
@router.get("/articles", response_model=list[PostResponse], include_in_schema=False)
def list_posts_route(db: Session = Depends(get_db)):
    return list_posts(db)


@router.get("/posts/{slug}", response_model=PostResponse)
@router.get("/articles/{slug}", response_model=PostResponse, include_in_schema=False)
def get_post_route(slug: str, db: Session = Depends(get_db)):
    post = get_post_by_slug(db, slug)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post
