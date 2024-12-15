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


logger = logging.getLogger("integrations service")

logfire.configure(send_to_logfire='if-token-present', token=settings.LOGFIRE_TOKEN, )

if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    #generate_unique_id_function=custom_generate_unique_id,
)



# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    allow_origins = [str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS]
else:
    allow_origins = ["*"]


class IgnoreReadinessProbeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if request.url.path == "/":
            # Ignora o readiness probe sem logar
            return await call_next(request)
        # Loga requisições para outros endpoints
        response = await call_next(request)

        logfire.instrument_fastapi(app)

        logger.info(f"Request path: {request.url.path} status code: {response.status_code}")
        return response

app.add_middleware(IgnoreReadinessProbeMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def readines_probe():
    return {"status": "ready"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
