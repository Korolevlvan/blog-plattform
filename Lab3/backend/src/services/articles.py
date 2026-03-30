from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.article import Post
from src.schemas.article import PostCreate
from src.tasks.celery_client import celery_app


def _make_unique_slug(db: Session, title: str) -> str:
    base_slug = slugify(title) or "post"
    slug = base_slug
    counter = 1
    while db.scalar(select(Post).where(Post.slug == slug)) is not None:
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


def create_post(db: Session, payload: PostCreate, author_id: int) -> Post:
    post = Post(
        title=payload.title,
        description=payload.description,
        body=payload.body,
        slug=_make_unique_slug(db, payload.title),
        tag_list=payload.tag_list,
        user_id=author_id,
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    celery_app.send_task(
        "notify_followers",
        kwargs={"author_id": author_id, "post_id": post.id},
    )
    return post


def list_posts(db: Session) -> list[Post]:
    return list(db.scalars(select(Post).order_by(Post.id.desc())).all())


def get_post_by_slug(db: Session, slug: str) -> Post | None:
    return db.scalar(select(Post).where(Post.slug == slug))
