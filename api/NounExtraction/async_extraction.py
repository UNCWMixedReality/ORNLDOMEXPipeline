import os
import sys

from celery import Celery
from flask import current_app

sys.path.append("../")
from app.__main__ import (  # noqa: E402
    classify_directory,
    classify_single_file,
    classify_zip,
)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


current_app.config.update(
    CELERY_BROKER_URL="redis://celery_broker:6379",
    CELERY_RESULT_BACKEND="redis://celery_broker:6379",
)
celery = make_celery(current_app)


@celery.task()
def classify_new_zip(file_path: str):
    return classify_zip(file_path, raw_json=True)
