import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.models import db_helper
from api import router as api_router

from exceptions import custom_exception_handler, NotFoundException, BadRequestException
from middleware import add_process_time_header


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