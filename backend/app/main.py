"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import health
from app.core.config import settings

from app.middleware.correlation import CorrelationMiddleware
app.add_middleware(CorrelationMiddleware)
from app.core.logging_config import setup_logging
setup_logging()

from app.api.v1.endpoints import auth
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])

from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=settings.API_V1_STR, tags=["health"])