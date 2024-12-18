from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from core.schemas.user import UserRead, UserUpdatePartial
from dependencies.user_dependencies import get_user_service
from services.user_service import UserService

router = APIRouter(tags=["User"])


@router.patch("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def patch_user(
    user_id: int,
    user: UserUpdatePartial,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.update_user_partial(user_id, user)
