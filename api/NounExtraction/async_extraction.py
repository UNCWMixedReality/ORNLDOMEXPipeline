# NOTE: Straight up, this script will most likely not run outside of a container

import os
import sys
import time

from celery import Celery
from DocumentExtraction.__main__ import (
    classify_directory,
    classify_single_file,
    classify_zip,
)

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@celery.task(name="classify_new_zip")
def classify_new_zip(file_path: str):
    return classify_zip(
        file_path,
        raw_json=True,
        db_config=os.path.abspath("NounExtraction/config.yaml"),
    )


@celery.task(name="classify_new_file")
def classify_new_file(file_path: str):
    return classify_single_file(
        file_path,
        raw_json=True,
        db_config=os.path.abspath("NounExtraction/config.yaml"),
    )


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


if os.environ.get("DEBUG", False):
    print("Ooooh someones having a bad day. Here's some info")
    print("=================================================")
    print(f"{sys.path = }")
    print(f"{os.getcwd() = }")
    print(f"{os.listdir() = }")
    print("=================================================\n\n")
