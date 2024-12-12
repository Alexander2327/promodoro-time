from typing import Annotated

from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from auth import utils as auth_utils
from core.schemas.auth import TokenInfo
from core.schemas.user import UserCreate
from dependencies.user_dependencies import get_user_service

from services.user_service import UserService

router = APIRouter(
    tags=["Auth"]
)


@router.post('/login', response_model=TokenInfo)
async def loging_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = await user_service.authenticate_user(
        username=form_data.username,
        password=form_data.password,
    )
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
    }
    token = auth_utils.encode_jwt(jwt_payload)

    return TokenInfo(access_token=token, token_type="Bearer")


@router.post("/register", response_model=TokenInfo, status_code=status.HTTP_201_CREATED)
async def post_user(
        user_create: UserCreate,
        user_service: Annotated[UserService, Depends(get_user_service)],
    ):
    user = await user_service.add_user(user_create)
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")
