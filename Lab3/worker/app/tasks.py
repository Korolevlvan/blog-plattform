import logging

import requests
from celery.utils.log import get_task_logger
from sqlalchemy import and_, select

from app.celery_app import celery
from app.config import settings
from app.db import MainSessionLocal, UsersSessionLocal
from app.models_main import Post
from app.models_users import NotificationSent, Subscriber, User

logger = get_task_logger(__name__)
logging.basicConfig(level=logging.INFO)


@celery.task(
    bind=True,
    name="notify_followers",
    autoretry_for=(requests.RequestException,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def notify_followers(self, author_id: int, post_id: int):
    task_id = getattr(self.request, "id", None)
    logger.info("start job task_id=%s author_id=%s post_id=%s", task_id, author_id, post_id)

    main_db = MainSessionLocal()
    users_db = UsersSessionLocal()
    try:
        post = main_db.scalar(select(Post).where(Post.id == post_id))
        if post is None:
            logger.warning("post not found task_id=%s post_id=%s", task_id, post_id)
            return {"status": "missing-post"}

        rows = users_db.execute(
            select(Subscriber.subscriber_id, User.subscription_key)
            .join(User, User.id == Subscriber.subscriber_id)
            .where(Subscriber.author_id == author_id)
        ).all()

        for subscriber_id, subscription_key in rows:
            existing = users_db.scalar(
                select(NotificationSent).where(
                    and_(
                        NotificationSent.subscriber_id == subscriber_id,
                        NotificationSent.post_id == post_id,
                    )
                )
            )
            if existing is not None:
                logger.info(
                    "skip duplicate task_id=%s subscriber_id=%s post_id=%s",
                    task_id,
                    subscriber_id,
                    post_id,
                )
                continue

            if not subscription_key:
                logger.warning(
                    "skip no-key task_id=%s subscriber_id=%s author_id=%s",
                    task_id,
                    subscriber_id,
                    author_id,
                )
                continue

            message = f"Пользователь {author_id} выпустил новый пост: {post.title[:10]}..."
            response = requests.post(
                settings.push_url,
                headers={
                    "Authorization": f"Bearer {subscription_key}",
                    "Content-Type": "application/json",
                },
                json={"message": message},
                timeout=5,
            )
            response.raise_for_status()

            users_db.add(NotificationSent(subscriber_id=subscriber_id, post_id=post_id, task_id=task_id))
            users_db.commit()
            logger.info(
                "sent task_id=%s subscriber_id=%s post_id=%s",
                task_id,
                subscriber_id,
                post_id,
            )

        return {"status": "ok"}
    finally:
        main_db.close()
        users_db.close()
