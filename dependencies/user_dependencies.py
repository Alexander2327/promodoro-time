from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from auth.utils import decode_jwt
from core.schemas.user import UserAuth
from exceptions.exception import UnauthorizedException
from services.user_service import UserService
from utils.unitofwork import IUnitOfWork, UnitOfWork

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='api/v1/auth/login')


async def get_user_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> UserService:
    return UserService(uow)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = decode_jwt(token)
        username: str = payload.get('username')
        user_id: str = payload.get('sub')
        if user_id is None or username is None:
            raise UnauthorizedException(detail='Unauthorized')
        return UserAuth(username=username, id=int(user_id))
    except jwt.exceptions.PyJWTError as e:
        raise UnauthorizedException(detail='Unauthorized')
