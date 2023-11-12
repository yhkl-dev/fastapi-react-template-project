from celery import Celery
from .config import settings


celery_app = Celery(
    "project",
)
celery_app.conf.result_backend = settings.CELERY_BACKEND_URL
celery_app.conf.broker_url = settings.CELERY_BROKER_URL

celery_app.conf.task_routes = {"project.tasks.*": "main-queue"}
celery_app.conf.beat_schedule = {
    "add-every-30-seconds": {
        "task": "project.tasks.add",
        "schedule": 30.0,
        "args": (16, 16),
    },
}
celery_app.set_default()
