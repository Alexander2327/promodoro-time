from typing import Annotated

from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from auth import utils as auth_utils
from core.schemas.auth import TokenInfo
from core.schemas.user import UserCreate
from dependencies.auth_dependencies import get_auth_service

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
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
    }
    token = auth_utils.encode_jwt(jwt_payload)

    return TokenInfo(access_token=token, token_type="Bearer")


@router.post("/register", response_model=TokenInfo, status_code=status.HTTP_201_CREATED)
async def post_user(
        user_create: UserCreate,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
    ):
    user = await auth_service.add_user(user_create)
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")
