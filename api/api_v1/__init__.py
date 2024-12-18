from fastapi import APIRouter

from core.config import settings

from .tasks import router as tasks_router
from .categories import router as categories_router
from .auth import router as auth_router
from .user import router as user_router

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
router.include_router(
    auth_router,
    prefix=settings.api.v1.auth,
)
router.include_router(
    user_router,
    prefix=settings.api.v1.users,
)
