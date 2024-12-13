from typing import Annotated

from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from api.api_v1.helpers import create_access_token, create_refresh_token
from core.schemas.auth import TokenInfo
from core.schemas.user import UserCreate, UserAuth
from dependencies.auth_dependencies import get_auth_service
from dependencies.user_dependencies import get_current_user_for_refresh

from services.auth_service import AuthService

router = APIRouter(
    tags=["Auth"]
)


@router.post('/login', response_model=TokenInfo)
async def loging_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    user = await auth_service.authenticate_user(
        username=form_data.username,
        password=form_data.password,
    )
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
async def refresh_access_token(
        user: Annotated[UserAuth, Depends(get_current_user_for_refresh)],
):
    access_token = create_access_token(user)
    return TokenInfo(access_token=access_token)


@router.post("/register", response_model=TokenInfo, status_code=status.HTTP_201_CREATED)
async def post_user(
        user_create: UserCreate,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    user = await auth_service.add_user(user_create)
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)
