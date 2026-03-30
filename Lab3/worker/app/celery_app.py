from celery import Celery

from app.config import settings

celery = Celery("lab3-worker", broker=settings.redis_url, backend=settings.redis_url)
celery.conf.task_default_queue = "notify"
celery.conf.task_routes = {"notify_followers": {"queue": "notify"}}
celery.conf.worker_prefetch_multiplier = 1

import app.tasks  # noqa: E402,F401
