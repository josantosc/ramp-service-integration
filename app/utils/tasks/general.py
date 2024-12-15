from app.core.config import settings
from fastapi import status, HTTPException


def get_task(
        client: int):
    try:
        client_tasks = {
            int(settings.ID_SANTO_ANDRE): "schedule-task-campaign-fd-sdr",
            int(settings.ID_RAMPED): "schedule-task-campaign-fd-ramped",
            int(settings.ID_IPATINGA): "schedule-task-campaign-fd-ipating",
            int(settings.ID_POA): "schedule-task-campaign-fd-poa",
            int(settings.ID_OSASCO): "schedule-task-campaign-fd-osasco",
            int(settings.ID_PINHEIROS): "schedule-task-campaign-fd-pinheiros",
            int(settings.ID_RK): "schedule-task-campaign-rk",
        }
        task = client_tasks.get(client)
        if task is None:
            raise ValueError(f"Client not found: {client}")
        return task
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


def normalize_task_name(client_name: str) -> str:
    normalized_name = client_name.lower().replace(" ", "-")
    return f"schedule-task-campaign-{normalized_name}"
