import logging
from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from api import router as api_router
from core.config import settings
from core.models import db_helper
from exceptions import (BadRequestException, NotFoundException,
                        custom_exception_handler)
from middleware import add_process_time_header

sentry_sdk.init(
    dsn="https://d7cd67a8f52b89d14aa28f2da0de9536@o4508489346121728.ingest.de.sentry.io/4508489350971472",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)
logging.basicConfig(
    # level=logging.INFO
    format=settings.logging.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    await db_helper.dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    title=settings.project.name,
    version=settings.project.version,
    description=settings.project.description,
)

main_app.include_router(
    api_router,
)

main_app.exception_handler(NotFoundException)(custom_exception_handler)
main_app.exception_handler(BadRequestException)(custom_exception_handler)

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
main_app.middleware("http")(add_process_time_header)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
