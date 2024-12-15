import json
from datetime import datetime
from typing import AnyStr
from uuid import uuid4
from enum import Enum
import logging

from app.adapters.celery import send_task
from app.core.config import settings


class EventCode(Enum):
    start_campaign = 100


class CampaignStatus(Enum):
    STARTED = 1
    COMPLETED = 2
    SCHEDULED = 3
    ERROR = 4
    STOPPED = 5
    PARTIAL = 6
    CANCELED = 7


async def send_event(
        event_code: Enum,
        task: str = None,
        queue: str = None,
        task_body: dict = None,
        task_eta=None
):
    try:
        if task:
            await send_task(task="mark-event", queue=f"{settings.ENV_SERVER}-events-validators",
                            body={"protocol": task_body.get("protocol"), "event_code": event_code.value})

            logging.info(f"TASK: {task_body} - QUEUE: {queue} - EVENT_CODE: {event_code.value}")

            await send_task(task=task, queue=queue, body=task_body, eta=task_eta)
            logging.info(f"TASK: {task_body} - QUEUE: {queue} - EVENT_CODE: {event_code.value}")

    except Exception as exc:
        logging.error(f"Error to send bot events: {str(exc)}")
