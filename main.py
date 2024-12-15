import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import logfire
import logging

from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


logfire.configure(send_to_logfire='if-token-present', token=settings.LOGFIRE_TOKEN, )

if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    #generate_unique_id_function=custom_generate_unique_id,
)

#logfire.instrument_fastapi(app)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    allow_origins = [str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS]
else:
    allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def readines_probe():
    return {"status": "ready"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
