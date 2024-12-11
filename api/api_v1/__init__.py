from fastapi import APIRouter

from core.config import settings

from .tasks import router as tasks_router
from .categories import router as categories_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    tasks_router,
    prefix=settings.api.v1.tasks,
)
router.include_router(
    categories_router,
    prefix=settings.api.v1.categories,
)