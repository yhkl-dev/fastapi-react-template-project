from project.celery_app import celery_app


@celery_app.task
def add(x: int, y: int) -> int:
    print(x + y)
    return x + y
