from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from api.api_v1.helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from auth.utils import decode_jwt
from core.schemas.user import UserAuth
from exceptions.exception import UnauthorizedException
from services.user_service import UserService
from utils.unitofwork import IUnitOfWork, UnitOfWork

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_user_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> UserService:
    return UserService(uow)


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type: str = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise UnauthorizedException(
        detail=f"Invalid token type: {current_token_type!r} expected {token_type!r}"
    )


def validate_token_user_data(payload: dict) -> bool:
    try:
        username: str = payload.get("username")
        user_id: str = payload.get("sub")
        if user_id is None or username is None:
            raise UnauthorizedException(detail="Unauthorized")
        return UserAuth(username=username, id=int(user_id))
    except jwt.exceptions.PyJWTError as e:
        raise UnauthorizedException(detail="Unauthorized")


# async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
#     try:
#         payload = decode_jwt(token)
#     except jwt.exceptions.PyJWTError as e:
#         raise UnauthorizedException(detail="Unauthorized")
#     validate_token_type(payload, ACCESS_TOKEN_TYPE)
#     return validate_token_user_data(payload)
#
#
# async def get_current_user_for_refresh(token: Annotated[str, Depends(oauth2_bearer)]):
#     try:
#         payload = decode_jwt(token)
#     except jwt.exceptions.PyJWTError as e:
#         raise UnauthorizedException(detail="Unauthorized")
#     validate_token_type(payload, REFRESH_TOKEN_TYPE)
#     return validate_token_user_data(payload)


def get_current_user_from_token_type(token_type: str):
    def get_current_user_from_token(token: Annotated[str, Depends(oauth2_bearer)]):
        try:
            payload = decode_jwt(token)
        except jwt.exceptions.PyJWTError as e:
            raise UnauthorizedException(detail="Unauthorized")
        validate_token_type(payload, token_type)
        return validate_token_user_data(payload)

    return get_current_user_from_token


get_current_user = get_current_user_from_token_type(ACCESS_TOKEN_TYPE)
get_current_user_for_refresh = get_current_user_from_token_type(REFRESH_TOKEN_TYPE)
