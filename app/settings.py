from decouple import config
from celery import Celery

CELERY = {
    "CELERY_BROKER_URL": config("CELERY_BROKER_URL"),
    "RESULT_BACKEND": config("RESULT_BACKEND"),
    "TASK_TIME_LIMIT": config("CELERYD_TASK_TIME_LIMIT", default=60),
    "TASK_IGNORE_RESULT": False,
    "TIMEZONE": "America/Sao_Paulo",
    "CELERY_ENABLE_UTC": True,
    "TASK_SEND_SENT_EVENT": True,
    "TASK_ACKS_LATE": True,
    "WORKER_PREFETCH_MULTIPLIER": 1,
    "TASK_COMPRESSION": "gzip",
    "RESULT_EXPIRES": config("CELERY_RESULT_EXPIRES", default=600, cast=int)
}

celery_app = Celery(__name__, config_source=CELERY)
