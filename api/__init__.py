from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core.config import settings
from .api_v1 import router as router_api_v1

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.prefix,
    dependencies=[Depends(http_bearer)],
)
router.include_router(router_api_v1)
