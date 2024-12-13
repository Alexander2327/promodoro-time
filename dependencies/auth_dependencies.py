from fastapi import Depends

from services.auth_service import AuthService
from utils.unitofwork import IUnitOfWork, UnitOfWork


async def get_auth_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> AuthService:
    return AuthService(uow)