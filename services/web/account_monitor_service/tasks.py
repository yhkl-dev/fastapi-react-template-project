from celery import shared_task
import datetime


@shared_task
def test_task() -> None:
    print("start collect analyze log from sumologic interface: ", datetime.datetime.now())

    print("save done")


@shared_task
def detect_new_accounts():
    print("this function is calling azure AD to detect new accounts information")
