from celery import Celery

from app.config import settings

celery = Celery(
    "tasks", broker=f"redis://{settings.REDIS_HOST}:6379", include=["app.tasks.tasks"]
)


# export TZ="UTC"
# celery -A app.tasks.celery_app:celery worker --loglevel=INFO
# celery -A app.tasks.celery_app:celery flower
