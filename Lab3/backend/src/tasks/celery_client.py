from celery import Celery

from src.core.config import settings

celery_app = Celery("backend-producer", broker=settings.redis_url)
